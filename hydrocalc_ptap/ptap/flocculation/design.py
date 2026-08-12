"""
Módulo de diseño de floculación para HYDROCALC-PTAP

Calcula:
- Volumen del floculador
- Potencia requerida
- Número de Camp (GT)
- Dimensiones del tanque
- Verificaciones de diseño

Referencias:
- AWWA M37 - Operational Control of Coagulation and Filtration Processes
- ASCE - Water Treatment Plant Design
- Camp, T. R., & Stein, P. C. (1943). Velocity gradients and internal work in fluid motion.
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Tuple
import numpy as np

from core.units import convert, convert_to_si, format_value
from core.constants import (
    DEFAULT_WATER_VISCOSITY,
    FLOCCULATION_PARAMS,
    check_parameter_range,
    get_design_parameter
)
from core.validation import (
    PTAPValidator,
    ValidationResult,
    ValidationLevel,
    validate_calculation
)


@dataclass
class FlocculationInput:
    """Datos de entrada para diseño de floculación"""
    flow: float  # Caudal
    detention_time: float  # Tiempo de retención
    velocity_gradient: float  # Gradiente de velocidad G
    
    flow_unit: str = "L_s"
    time_unit: str = "min"
    gradient_unit: str = "s-1"
    
    water_temperature: float = 20.0  # °C
    num_chambers: int = 3  # Número de cámaras en serie
    
    # Parámetros opcionales
    viscosity: Optional[float] = None  # Si None, se calcula de la temperatura
    width_depth_ratio: float = 1.5  # Relación ancho/profundidad


@dataclass
class FlocculationResult:
    """Resultados del diseño de floculación"""
    # Resultados principales
    volume: float = 0.0  # m³
    power: float = 0.0  # W
    gt_number: float = 0.0  # Adimensional
    
    # Parámetros calculados
    velocity_gradient_si: float = 0.0  # s⁻¹
    detention_time_si: float = 0.0  # s
    flow_si: float = 0.0  # m³/s
    
    # Geometría
    total_volume: float = 0.0  # m³ (volumen total considerando cámaras)
    volume_per_chamber: float = 0.0  # m³
    dimensions: Optional[Dict[str, float]] = None
    
    # Unidades
    volume_SI_unit: str = "m³"
    power_SI_unit: str = "W"
    
    # Validaciones
    validation_result: Optional[ValidationResult] = None
    
    # Información adicional
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convertir resultado a diccionario"""
        return {
            'volume': self.volume,
            'volume_unit': self.volume_SI_unit,
            'power': self.power,
            'power_unit': self.power_SI_unit,
            'gt_number': self.gt_number,
            'velocity_gradient': self.velocity_gradient_si,
            'detention_time': self.detention_time_si,
            'flow': self.flow_si,
            'total_volume': self.total_volume,
            'volume_per_chamber': self.volume_per_chamber,
            'dimensions': self.dimensions,
            'validation': self.validation_result.to_dict() if self.validation_result else None,
            'warnings': self.warnings,
            'info': self.info
        }


def get_water_viscosity(temperature: float) -> float:
    """
    Obtener viscosidad dinámica del agua para una temperatura dada
    
    Usa correlación empírica basada en datos estándar
    
    Args:
        temperature: Temperatura en °C
    
    Returns:
        Viscosidad dinámica en Pa·s
    """
    # Correlación empírica para viscosidad del agua
    # Basada en datos del NIST
    if temperature < 0 or temperature > 100:
        # Fuera de rango, usar valor por defecto
        return DEFAULT_WATER_VISCOSITY
    
    # Ecuación de Vogel-Fulcher-Tammann modificada
    A = 2.414e-5  # Pa·s
    B = 247.8  # K
    C = 140  # K
    
    T_K = temperature + 273.15  # Convertir a Kelvin
    viscosity = A * 10 ** (B / (T_K - C))
    
    return viscosity


def calculate_flocculator_volume(flow_si: float, detention_time_si: float) -> float:
    """
    Calcular volumen del floculador
    
    Ecuación fundamental:
    V = Q × T
    
    Args:
        flow_si: Caudal en m³/s
        detention_time_si: Tiempo de retención en segundos
    
    Returns:
        Volumen en m³
    """
    return flow_si * detention_time_si


def calculate_mixing_power(viscosity: float, velocity_gradient: float, 
                           volume: float) -> float:
    """
    Calcular potencia requerida para mezcla
    
    Ecuación de Camp-Stein:
    P = μ × G² × V
    
    Donde:
    P = Potencia [W]
    μ = Viscosidad dinámica [Pa·s]
    G = Gradiente de velocidad [s⁻¹]
    V = Volumen [m³]
    
    Args:
        viscosity: Viscosidad dinámica en Pa·s
        velocity_gradient: Gradiente de velocidad en s⁻¹
        volume: Volumen en m³
    
    Returns:
        Potencia en W
    """
    return viscosity * (velocity_gradient ** 2) * volume


def calculate_gt_number(velocity_gradient: float, detention_time: float) -> float:
    """
    Calcular número de Camp (GT)
    
    GT = G × T
    
    Este parámetro adimensional es fundamental para el diseño
    de procesos de coagulación-floculación.
    
    Rangos típicos:
    - Mezcla rápida: 10,000 - 60,000
    - Floculación: 20,000 - 200,000
    
    Args:
        velocity_gradient: Gradiente de velocidad en s⁻¹
        detention_time: Tiempo de retención en segundos
    
    Returns:
        Número de Camp (adimensional)
    """
    return velocity_gradient * detention_time


def estimate_dimensions(volume: float, width_depth_ratio: float = 1.5,
                        num_chambers: int = 3) -> Dict[str, float]:
    """
    Estimar dimensiones preliminares del floculador
    
    Asume un tanque rectangular con relación ancho/profundidad fija
    
    Args:
        volume: Volumen total en m³
        width_depth_ratio: Relación ancho/profundidad
        num_chambers: Número de cámaras en serie
    
    Returns:
        Diccionario con dimensiones estimadas
    """
    volume_per_chamber = volume / num_chambers
    
    # Suponiendo relación L:W:D típica para floculadores
    # Usualmente L/W ≈ 3-4 para flujo horizontal
    length_width_ratio = 3.5
    
    # Volumen = L × W × D
    # W = ratio × D
    # L = LW_ratio × W = LW_ratio × ratio × D
    # V = (LW_ratio × ratio × D) × (ratio × D) × D
    # V = LW_ratio × ratio² × D³
    
    depth = (volume_per_chamber / (length_width_ratio * width_depth_ratio**2)) ** (1/3)
    width = width_depth_ratio * depth
    length = length_width_ratio * width
    
    return {
        'depth': depth,
        'width': width,
        'length': length,
        'length_total': length * num_chambers,
        'volume_per_chamber': volume_per_chamber,
        'num_chambers': num_chambers
    }


def design_flocculation(inputs: FlocculationInput) -> FlocculationResult:
    """
    Función principal de diseño de floculación
    
    Realiza todos los cálculos necesarios para el diseño preliminar
    de un sistema de floculación.
    
    Args:
        inputs: Datos de entrada
    
    Returns:
        FlocculationResult con todos los resultados
    """
    result = FlocculationResult(
        volume=0,
        power=0,
        gt_number=0,
        velocity_gradient_si=0,
        detention_time_si=0,
        flow_si=0,
        total_volume=0,
        volume_per_chamber=0
    )
    
    # =========================================================================
    # PASO 1: CONVERSIÓN DE UNIDADES A SI
    # =========================================================================
    
    try:
        flow_si, flow_unit_si = convert_to_si(inputs.flow, inputs.flow_unit)
        result.flow_si = flow_si
        
        detention_time_si, time_unit_si = convert_to_si(
            inputs.detention_time, inputs.time_unit
        )
        result.detention_time_si = detention_time_si
        
        gradient_si, gradient_unit_si = convert_to_si(
            inputs.velocity_gradient, inputs.gradient_unit
        )
        result.velocity_gradient_si = gradient_si
        
    except Exception as e:
        result.validation_result = ValidationResult(is_valid=False)
        result.validation_result.add_critical(
            "unidades",
            f"Error en conversión de unidades: {str(e)}"
        )
        return result
    
    # =========================================================================
    # PASO 2: OBTENER PROPIEDADES DEL AGUA
    # =========================================================================
    
    if inputs.viscosity is not None:
        viscosity = inputs.viscosity
    else:
        viscosity = get_water_viscosity(inputs.water_temperature)
    
    result.info.append(
        f"Viscosidad del agua a {inputs.water_temperature}°C: {viscosity:.4e} Pa·s"
    )
    
    # =========================================================================
    # PASO 3: VALIDACIÓN DE DATOS DE ENTRADA
    # =========================================================================
    
    validation_rules = {
        'flow': 'flow',
        'detention_time': 'time',
        'velocity_gradient': 'gradient'
    }
    
    validation_inputs = {
        'flow': inputs.flow,
        'detention_time': inputs.detention_time,
        'velocity_gradient': inputs.velocity_gradient
    }
    
    validation_result = validate_calculation(validation_inputs, validation_rules)
    
    # Validación específica para floculación
    gt_check = check_parameter_range('flocculation', 'G', inputs.velocity_gradient)
    if not gt_check['in_range'] and gt_check['warning']:
        validation_result.add_warning(
            'velocity_gradient',
            gt_check['warning'],
            suggestion="Verificar criterios de diseño"
        )
    
    result.validation_result = validation_result
    
    # Si hay errores críticos, detener cálculo
    if not validation_result.is_valid:
        errors = validation_result.get_errors()
        if any(e.level == ValidationLevel.CRITICAL for e in errors):
            return result
    
    # =========================================================================
    # PASO 4: CÁLCULOS PRINCIPALES
    # =========================================================================
    
    # Volumen del floculador
    volume = calculate_flocculator_volume(flow_si, detention_time_si)
    result.volume = volume
    
    # Potencia requerida
    power = calculate_mixing_power(viscosity, gradient_si, volume)
    result.power = power
    
    # Número de Camp
    gt = calculate_gt_number(gradient_si, detention_time_si)
    result.gt_number = gt
    
    # =========================================================================
    # PASO 5: GEOMETRÍA Y CONFIGURACIÓN
    # =========================================================================
    
    result.total_volume = volume
    result.volume_per_chamber = volume / inputs.num_chambers
    
    # Estimar dimensiones
    dimensions = estimate_dimensions(
        volume,
        inputs.width_depth_ratio,
        inputs.num_chambers
    )
    result.dimensions = dimensions
    
    # =========================================================================
    # PASO 6: VERIFICACIONES ADICIONALES
    # =========================================================================
    
    # Verificar número de Camp
    gt_validation = check_parameter_range('flocculation', 'GT', gt)
    if gt_validation['warning']:
        result.warnings.append(gt_validation['warning'])
    else:
        result.info.append(f"Número de Camp (GT) dentro del rango recomendado: {gt:.0f}")
    
    # Verificar potencia
    if power < 10:
        result.info.append(
            f"Potencia muy baja ({power:.2f} W). Verificar si requiere agitación mecánica o hidráulica."
        )
    elif power > 10000:
        result.warnings.append(
            f"Potencia elevada ({power/1000:.2f} kW). Considerar múltiples unidades."
        )
    
    # Agregar información de conversión
    result.info.append(
        f"Caudal: {format_value(inputs.flow, inputs.flow_unit)} = {format_value(flow_si, 'm3_s')}"
    )
    result.info.append(
        f"Tiempo: {format_value(inputs.detention_time, inputs.time_unit)} = {format_value(detention_time_si, 's')}"
    )
    result.info.append(
        f"Gradiente G: {format_value(inputs.velocity_gradient, inputs.gradient_unit)} = {format_value(gradient_si, 's-1')}"
    )
    
    return result


def calculate_staged_flocculation(
    flow: float,
    total_detention_time: float,
    initial_G: float,
    final_G: float,
    num_stages: int = 3,
    flow_unit: str = "L_s",
    time_unit: str = "min"
) -> Dict[str, List[float]]:
    """
    Calcular floculación escalonada con gradiente decreciente
    
    En la práctica, los floculadores modernos usan gradientes decrecientes
    para optimizar la formación de flóculos y minimizar su ruptura.
    
    Args:
        flow: Caudal
        total_detention_time: Tiempo total de retención
        initial_G: Gradiente inicial (primera etapa)
        final_G: Gradiente final (última etapa)
        num_stages: Número de etapas
        flow_unit: Unidad de caudal
        time_unit: Unidad de tiempo
    
    Returns:
        Diccionario con listas de parámetros por etapa
    """
    # Convertir a SI
    flow_si, _ = convert_to_si(flow, flow_unit)
    time_si, _ = convert_to_si(total_detention_time, time_unit)
    
    # Calcular gradiente para cada etapa (decaimiento lineal o exponencial)
    # Usaremos decaimiento lineal como aproximación
    G_values = np.linspace(initial_G, final_G, num_stages)
    
    # Tiempo por etapa (asumiendo distribución igualitaria)
    T_per_stage = time_si / num_stages
    
    # Calcular parámetros por etapa
    results = {
        'stage': list(range(1, num_stages + 1)),
        'G': G_values.tolist(),
        'T': [T_per_stage] * num_stages,
        'V': [],
        'P': [],
        'GT_stage': [],
    }
    
    viscosity = get_water_viscosity(20)  # Asumir 20°C
    
    cumulative_GT = 0
    for i in range(num_stages):
        G = G_values[i]
        T = T_per_stage
        
        # Volumen por etapa
        V = flow_si * T
        results['V'].append(V)
        
        # Potencia por etapa
        P = viscosity * (G ** 2) * V
        results['P'].append(P)
        
        # GT por etapa
        GT_stage = G * T
        cumulative_GT += GT_stage
        results['GT_stage'].append(GT_stage)
    
    results['GT_total'] = cumulative_GT
    results['G_average'] = np.mean(G_values)
    
    return results
