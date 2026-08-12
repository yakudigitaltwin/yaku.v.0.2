"""
Módulo de dosificación de coagulantes para HYDROCALC-PTAP

Calcula:
- Dosis de coagulante
- Concentración de solución
- Caudal de dosificación
- Consumo diario/mensual/anual
- Verificaciones de diseño

Referencias:
- AWWA M37 - Operational Control of Coagulation and Filtration Processes
- ASCE - Water Treatment Plant Design
- WHO - Guidelines for Drinking-water Quality
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional
import numpy as np

from core.units import convert, convert_to_si, format_value
from core.constants import (
    CHEMICALS,
    get_chemical,
    list_chemicals,
    calculate_dosage_mass,
)
from core.validation import (
    ValidationResult,
    ValidationLevel,
    validate_calculation,
)


@dataclass
class CoagulantDosageInput:
    """Datos de entrada para cálculo de dosificación"""
    flow: float  # Caudal de agua a tratar
    dose: float  # Dosis de coagulante
    chemical_name: str  # Nombre del coagulante
    
    flow_unit: str = "L_s"
    dose_unit: str = "mg_L"
    
    # Parámetros opcionales
    solution_concentration: Optional[float] = None  # % p/p o g/L
    purity: Optional[float] = None  # % pureza del químico
    operating_hours: float = 24.0  # Horas de operación por día


@dataclass
class CoagulantDosageResult:
    """Resultados del cálculo de dosificación"""
    # Resultados principales
    daily_mass: float  # kg/día
    hourly_mass: float  # kg/hora
    
    # Solución química
    solution_flow_rate: Optional[float] = None  # L/h o mL/min
    solution_flow_unit: Optional[str] = None
    
    # Parámetros del químico
    chemical_info: Optional[Dict] = None
    purity_used: float = 100.0
    
    # Validaciones
    validation_result: Optional[ValidationResult] = None
    
    # Información adicional
    warnings: List[str] = field(default_factory=list)
    info: List[str] = field(default_factory=list)
    
    def to_dict(self) -> dict:
        """Convertir resultado a diccionario"""
        return {
            'daily_mass': self.daily_mass,
            'hourly_mass': self.hourly_mass,
            'solution_flow_rate': self.solution_flow_rate,
            'solution_flow_unit': self.solution_flow_unit,
            'chemical_info': self.chemical_info,
            'purity_used': self.purity_used,
            'validation': self.validation_result.to_dict() if self.validation_result else None,
            'warnings': self.warnings,
            'info': self.info
        }


def calculate_daily_consumption(flow_si: float, dose_si: float, 
                                purity: float = 100.0) -> tuple[float, float]:
    """
    Calcular consumo diario de coagulante
    
    Fórmulas:
    Masa diaria (kg/d) = Q (m³/d) × Dosis (mg/L) / (Pureza × 1000)
    Masa horaria (kg/h) = Masa diaria / 24
    
    Args:
        flow_si: Caudal en m³/día
        dose_si: Dosis en mg/L (que es equivalente a g/m³)
        purity: Pureza del químico en %
    
    Returns:
        Tupla (masa_diaria_kg, masa_horaria_kg)
    """
    # Q (m³/d) × Dosis (mg/L) = g/d
    # Porque: m³/d × mg/L = m³/d × g/m³ = g/d
    mass_per_day_g = flow_si * dose_si
    
    # Convertir a kg y ajustar por pureza
    mass_per_day_kg = (mass_per_day_g / 1000) / (purity / 100)
    
    # Masa horaria
    mass_per_hour_kg = mass_per_day_kg / 24
    
    return mass_per_day_kg, mass_per_hour_kg


def calculate_solution_flow(daily_mass: float, solution_conc: float,
                            operating_hours: float = 24.0) -> tuple[float, str]:
    """
    Calcular caudal de solución coagulante
    
    Args:
        daily_mass: Masa diaria de coagulante puro (kg/d)
        solution_conc: Concentración de la solución (% p/p o g/L)
        operating_hours: Horas de operación del sistema de dosificación
    
    Returns:
        Tupla (caudal_solucion, unidad)
    """
    # Asumiendo solución al X% p/p
    # Si daily_mass es kg/d de químico puro
    # y queremos solución al C% p/p
    
    # Masa de solución necesaria (kg/d)
    solution_mass_per_day = daily_mass / (solution_conc / 100)
    
    # Asumiendo densidad ≈ 1 kg/L para soluciones diluidas
    solution_volume_per_day_L = solution_mass_per_day * 1000  # L/d
    
    # Caudal de solución
    solution_flow_L_h = solution_volume_per_day_L / operating_hours
    solution_flow_mL_min = (solution_flow_L_h * 1000) / 60  # mL/min
    
    return solution_flow_mL_min, "mL/min"


def calculate_dilution_ratio(stock_conc: float, target_conc: float) -> float:
    """
    Calcular relación de dilución necesaria
    
    Fórmula de dilución:
    C1 × V1 = C2 × V2
    
    Args:
        stock_conc: Concentración de la solución madre (%)
        target_conc: Concentración objetivo (%)
    
    Returns:
        Factor de dilución (V2/V1)
    """
    if target_conc >= stock_conc:
        raise ValueError(
            "La concentración objetivo debe ser menor que la concentración de stock"
        )
    
    dilution_factor = stock_conc / target_conc
    return dilution_factor


def calculate_coagulant_dosage(inputs: CoagulantDosageInput) -> CoagulantDosageResult:
    """
    Función principal para cálculo de dosificación de coagulante
    
    Args:
        inputs: Datos de entrada
    
    Returns:
        CoagulantDosageResult con todos los resultados
    """
    result = CoagulantDosageResult(
        daily_mass=0,
        hourly_mass=0,
        purity_used=100.0
    )
    
    # =========================================================================
    # PASO 1: OBTENER INFORMACIÓN DEL QUÍMICO
    # =========================================================================
    
    chemical = get_chemical(inputs.chemical_name)
    
    if chemical is None:
        result.validation_result = ValidationResult(is_valid=False)
        result.validation_result.add_critical(
            "chemical",
            f"Químico desconocido: {inputs.chemical_name}. "
            f"Químicos disponibles: {', '.join(list_chemicals())}"
        )
        return result
    
    result.chemical_info = {
        'name': chemical.name,
        'formula': chemical.formula,
        'molecular_weight': chemical.molecular_weight,
        'state': chemical.state,
        'application': chemical.application,
        'hazards': chemical.hazards
    }
    
    # Determinar pureza a usar
    if inputs.purity is not None:
        purity = inputs.purity
    else:
        purity = chemical.purity_typical
    
    result.purity_used = purity
    result.info.append(f"Pureza utilizada: {purity:.1f}%")
    
    # =========================================================================
    # PASO 2: CONVERSIÓN DE UNIDADES
    # =========================================================================
    
    try:
        # Convertir caudal a m³/día para cálculo de consumo
        flow_si, _ = convert_to_si(inputs.flow, inputs.flow_unit)
        flow_m3_d = flow_si * 86400  # m³/s → m³/d
        
        # La dosis en mg/L ya está en unidades convenientes
        dose_mg_L = inputs.dose
        
    except Exception as e:
        result.validation_result = ValidationResult(is_valid=False)
        result.validation_result.add_critical(
            "unidades",
            f"Error en conversión de unidades: {str(e)}"
        )
        return result
    
    # =========================================================================
    # PASO 3: VALIDACIÓN DE DATOS
    # =========================================================================
    
    validation_inputs = {
        'flow': inputs.flow,
        'dose': inputs.dose,
    }
    
    validation_rules = {
        'flow': 'flow',
        'dose': 'concentration'
    }
    
    validation_result = validate_calculation(validation_inputs, validation_rules)
    
    # Verificar rango de dosis típico para el químico
    min_dose, max_dose = chemical.dosage_range
    if dose_mg_L < min_dose or dose_mg_L > max_dose:
        validation_result.add_warning(
            'dose',
            f"Dosis {dose_mg_L} mg/L fuera del rango típico ({min_dose}-{max_dose} mg/L) "
            f"para {chemical.name}",
            suggestion="Verificar mediante jar test"
        )
    
    result.validation_result = validation_result
    
    if not validation_result.is_valid:
        errors = validation_result.get_errors()
        if any(e.level == ValidationLevel.CRITICAL for e in errors):
            return result
    
    # =========================================================================
    # PASO 4: CÁLCULOS PRINCIPALES
    # =========================================================================
    
    # Consumo diario y horario
    daily_mass, hourly_mass = calculate_daily_consumption(
        flow_m3_d, dose_mg_L, purity
    )
    
    result.daily_mass = daily_mass
    result.hourly_mass = hourly_mass
    
    # =========================================================================
    # PASO 5: CÁLCULO DE SOLUCIÓN (si se proporciona concentración)
    # =========================================================================
    
    if inputs.solution_concentration is not None:
        solution_flow, solution_unit = calculate_solution_flow(
            daily_mass,
            inputs.solution_concentration,
            inputs.operating_hours
        )
        
        result.solution_flow_rate = solution_flow
        result.solution_flow_unit = solution_unit
        
        result.info.append(
            f"Solución al {inputs.solution_concentration}%: "
            f"{solution_flow:.2f} {solution_unit}"
        )
    
    # =========================================================================
    # PASO 6: INFORMACIÓN ADICIONAL Y VERIFICACIONES
    # =========================================================================
    
    # Consumo mensual y anual estimado
    monthly_mass = daily_mass * 30
    annual_mass = daily_mass * 365
    
    result.info.extend([
        f"Consumo mensual estimado: {monthly_mass:.1f} kg/mes",
        f"Consumo anual estimado: {annual_mass:.1f} kg/año",
    ])
    
    # Verificaciones
    if daily_mass < 1:
        result.info.append(
            "Consumo bajo. Considerar tanques de solución más pequeños para mejor control."
        )
    elif daily_mass > 1000:
        result.warnings.append(
            f"Consumo elevado ({daily_mass:.1f} kg/d). Considerar almacenamiento a granel."
        )
    
    # Agregar información de seguridad
    if chemical.hazards:
        result.info.append(f"Precauciones: {', '.join(chemical.hazards)}")
    
    # Información de conversión
    result.info.append(
        f"Caudal: {format_value(inputs.flow, inputs.flow_unit)} = "
        f"{format_value(flow_m3_d, 'm3_h')}/d"
    )
    
    return result


def optimize_coagulant_dose(
    flow: float,
    dose_range: tuple,
    chemical_name: str,
    target_turbidity: Optional[float] = None,
    initial_turbidity: Optional[float] = None,
    flow_unit: str = "L_s"
) -> Dict:
    """
    Optimizar dosis de coagulante basándose en rangos
    
    Esta función evalúa múltiples dosis para encontrar la óptima
    desde el punto de vista económico y operativo.
    
    Args:
        flow: Caudal de agua
        dose_range: Tupla (dosis_min, dosis_max, paso) en mg/L
        chemical_name: Nombre del coagulante
        target_turbidity: Turbiedad objetivo (opcional)
        initial_turbidity: Turbiedad inicial (opcional)
        flow_unit: Unidad de caudal
    
    Returns:
        Diccionario con análisis de optimización
    """
    dose_min, dose_max, dose_step = dose_range
    
    # Generar array de dosis a evaluar
    doses = np.arange(dose_min, dose_max + dose_step, dose_step)
    
    results = []
    
    for dose in doses:
        inputs = CoagulantDosageInput(
            flow=flow,
            flow_unit=flow_unit,
            dose=dose,
            chemical_name=chemical_name
        )
        
        result = calculate_coagulant_dosage(inputs)
        
        if result.validation_result and result.validation_result.is_valid:
            results.append({
                'dose': dose,
                'daily_mass': result.daily_mass,
                'hourly_mass': result.hourly_mass,
                'valid': True
            })
    
    if not results:
        return {'error': 'No se pudieron calcular resultados válidos'}
    
    # Encontrar dosis óptima (mínimo consumo dentro del rango)
    optimal = min(results, key=lambda x: x['daily_mass'])
    maximum = max(results, key=lambda x: x['daily_mass'])
    
    return {
        'doses_evaluated': len(results),
        'dose_range': [dose_min, dose_max],
        'optimal_dose': optimal['dose'],
        'optimal_daily_consumption': optimal['daily_mass'],
        'maximum_daily_consumption': maximum['daily_mass'],
        'consumption_range': [
            optimal['daily_mass'],
            maximum['daily_mass']
        ],
        'all_results': results
    }


def calculate_chemical_requirements(
    flow: float,
    dose: float,
    chemical_name: str,
    storage_days: int = 30,
    safety_factor: float = 1.2,
    flow_unit: str = "L_s",
    dose_unit: str = "mg_L"
) -> Dict:
    """
    Calcular requerimientos completos de almacenamiento de químico
    
    Args:
        flow: Caudal
        dose: Dosis
        chemical_name: Nombre del químico
        storage_days: Días de almacenamiento deseado
        safety_factor: Factor de seguridad
        flow_unit: Unidad de caudal
        dose_unit: Unidad de dosis
    
    Returns:
        Diccionario con requerimientos de almacenamiento
    """
    # Calcular consumo básico
    inputs = CoagulantDosageInput(
        flow=flow,
        flow_unit=flow_unit,
        dose=dose,
        dose_unit=dose_unit,
        chemical_name=chemical_name
    )
    
    result = calculate_coagulant_dosage(inputs)
    
    if not result.validation_result or not result.validation_result.is_valid:
        return {'error': 'Cálculo no válido', 'details': result.validation_result}
    
    # Calcular almacenamiento necesario
    daily_consumption = result.daily_mass
    storage_capacity = daily_consumption * storage_days * safety_factor
    
    # Volumen de almacenamiento (asumiendo densidad del químico)
    chemical = get_chemical(chemical_name)
    if chemical:
        density = chemical.density  # kg/m³ para sólidos, o g/mL para líquidos
        
        if chemical.state == 'solid':
            # Para sólidos, volumen en m³
            storage_volume_m3 = storage_capacity / density
            storage_volume_L = storage_volume_m3 * 1000
        else:
            # Para líquidos, asumir solución concentrada
            # Densidad en kg/m³ → kg/L dividiendo por 1000
            density_kg_L = density / 1000
            storage_volume_L = storage_capacity / density_kg_L
    
        storage_info = {
            'storage_capacity_kg': storage_capacity,
            'storage_volume_L': storage_volume_L,
            'storage_volume_m3': storage_volume_L / 1000,
            'density': density,
            'state': chemical.state
        }
    else:
        storage_info = {
            'storage_capacity_kg': storage_capacity
        }
    
    return {
        'daily_consumption_kg': daily_consumption,
        'monthly_consumption_kg': daily_consumption * 30,
        'annual_consumption_kg': daily_consumption * 365,
        'storage_days': storage_days,
        'safety_factor': safety_factor,
        **storage_info,
        'chemical_info': result.chemical_info
    }
