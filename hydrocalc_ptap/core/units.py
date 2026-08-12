"""
Sistema de unidades para HYDROCALC-PTAP

Soporta conversión entre unidades comunes en ingeniería del agua:
- Caudal: L/s, m³/s, L/min, m³/h, GPM
- Volumen: L, m³, galones, ft³
- Tiempo: s, min, h, días
- Presión: Pa, kPa, bar, psi, mca
- Concentración: mg/L, g/L, kg/m³, ppm, %
- Potencia: W, kW, HP
- Viscosidad: Pa·s, mPa·s, cP
- Gradiente de velocidad: s⁻¹
"""

from dataclasses import dataclass
from typing import Dict, Union, Optional
from enum import Enum


class UnitType(Enum):
    """Tipos de unidades soportadas"""
    FLOW = "flow"  # Caudal
    VOLUME = "volume"  # Volumen
    TIME = "time"  # Tiempo
    PRESSURE = "pressure"  # Presión
    CONCENTRATION = "concentration"  # Concentración
    POWER = "power"  # Potencia
    VISCOSITY = "viscosity"  # Viscosidad
    GRADIENT = "gradient"  # Gradiente de velocidad
    LENGTH = "length"  # Longitud
    MASS = "mass"  # Masa


@dataclass
class UnitDefinition:
    """Definición de una unidad"""
    name: str
    symbol: str
    unit_type: UnitType
    to_si: float  # Factor de conversión a SI
    si_unit: str  # Unidad SI


# Definición de unidades
UNITS: Dict[str, UnitDefinition] = {
    # Caudal (SI: m³/s)
    "m3_s": UnitDefinition("metro cúbico por segundo", "m³/s", UnitType.FLOW, 1.0, "m³/s"),
    "L_s": UnitDefinition("litro por segundo", "L/s", UnitType.FLOW, 0.001, "m³/s"),
    "L_min": UnitDefinition("litro por minuto", "L/min", UnitType.FLOW, 0.001 / 60, "m³/s"),
    "m3_h": UnitDefinition("metro cúbico por hora", "m³/h", UnitType.FLOW, 1.0 / 3600, "m³/s"),
    "GPM": UnitDefinition("galón por minuto", "GPM", UnitType.FLOW, 6.309e-5, "m³/s"),
    
    # Volumen (SI: m³)
    "m3": UnitDefinition("metro cúbico", "m³", UnitType.VOLUME, 1.0, "m³"),
    "L": UnitDefinition("litro", "L", UnitType.VOLUME, 0.001, "m³"),
    "gal": UnitDefinition("galón", "gal", UnitType.VOLUME, 0.00378541, "m³"),
    "ft3": UnitDefinition("pie cúbico", "ft³", UnitType.VOLUME, 0.0283168, "m³"),
    
    # Tiempo (SI: s)
    "s": UnitDefinition("segundo", "s", UnitType.TIME, 1.0, "s"),
    "min": UnitDefinition("minuto", "min", UnitType.TIME, 60.0, "s"),
    "h": UnitDefinition("hora", "h", UnitType.TIME, 3600.0, "s"),
    "d": UnitDefinition("día", "d", UnitType.TIME, 86400.0, "s"),
    
    # Presión (SI: Pa)
    "Pa": UnitDefinition("pascal", "Pa", UnitType.PRESSURE, 1.0, "Pa"),
    "kPa": UnitDefinition("kilopascal", "kPa", UnitType.PRESSURE, 1000.0, "Pa"),
    "bar": UnitDefinition("bar", "bar", UnitType.PRESSURE, 100000.0, "Pa"),
    "psi": UnitDefinition("libra por pulgada cuadrada", "psi", UnitType.PRESSURE, 6894.76, "Pa"),
    "mca": UnitDefinition("metro de columna de agua", "mca", UnitType.PRESSURE, 9806.65, "Pa"),
    
    # Concentración (SI: kg/m³)
    "kg_m3": UnitDefinition("kilogramo por metro cúbico", "kg/m³", UnitType.CONCENTRATION, 1.0, "kg/m³"),
    "g_L": UnitDefinition("gramo por litro", "g/L", UnitType.CONCENTRATION, 1.0, "kg/m³"),
    "mg_L": UnitDefinition("miligramo por litro", "mg/L", UnitType.CONCENTRATION, 0.001, "kg/m³"),
    "ppm": UnitDefinition("partes por millón", "ppm", UnitType.CONCENTRATION, 0.001, "kg/m³"),
    "percent": UnitDefinition("porcentaje", "%", UnitType.CONCENTRATION, 10.0, "kg/m³"),
    
    # Potencia (SI: W)
    "W": UnitDefinition("watt", "W", UnitType.POWER, 1.0, "W"),
    "kW": UnitDefinition("kilowatt", "kW", UnitType.POWER, 1000.0, "W"),
    "HP": UnitDefinition("caballo de vapor", "HP", UnitType.POWER, 745.7, "W"),
    
    # Viscosidad (SI: Pa·s)
    "Pa_s": UnitDefinition("pascal-segundo", "Pa·s", UnitType.VISCOSITY, 1.0, "Pa·s"),
    "mPa_s": UnitDefinition("milipascal-segundo", "mPa·s", UnitType.VISCOSITY, 0.001, "Pa·s"),
    "cP": UnitDefinition("centipoise", "cP", UnitType.VISCOSITY, 0.001, "Pa·s"),
    
    # Gradiente de velocidad (SI: s⁻¹)
    "s-1": UnitDefinition("inverso de segundo", "s⁻¹", UnitType.GRADIENT, 1.0, "s⁻¹"),
    
    # Longitud (SI: m)
    "m": UnitDefinition("metro", "m", UnitType.LENGTH, 1.0, "m"),
    "cm": UnitDefinition("centímetro", "cm", UnitType.LENGTH, 0.01, "m"),
    "mm": UnitDefinition("milímetro", "mm", UnitType.LENGTH, 0.001, "m"),
    "ft": UnitDefinition("pie", "ft", UnitType.LENGTH, 0.3048, "m"),
    "in": UnitDefinition("pulgada", "in", UnitType.LENGTH, 0.0254, "m"),
    
    # Masa (SI: kg)
    "kg": UnitDefinition("kilogramo", "kg", UnitType.MASS, 1.0, "kg"),
    "g": UnitDefinition("gramo", "g", UnitType.MASS, 0.001, "kg"),
    "mg": UnitDefinition("miligramo", "mg", UnitType.MASS, 1e-6, "kg"),
    "lb": UnitDefinition("libra", "lb", UnitType.MASS, 0.453592, "kg"),
}


def get_unit(unit_code: str) -> UnitDefinition:
    """Obtener definición de unidad por código"""
    if unit_code not in UNITS:
        raise ValueError(f"Unidad desconocida: {unit_code}. Unidades disponibles: {list(UNITS.keys())}")
    return UNITS[unit_code]


def convert(value: float, from_unit: str, to_unit: str) -> float:
    """
    Convertir un valor de una unidad a otra
    
    Args:
        value: Valor numérico a convertir
        from_unit: Código de la unidad de origen
        to_unit: Código de la unidad de destino
    
    Returns:
        Valor convertido
    
    Raises:
        ValueError: Si las unidades son incompatibles o desconocidas
    """
    from_def = get_unit(from_unit)
    to_def = get_unit(to_unit)
    
    if from_def.unit_type != to_def.unit_type:
        raise ValueError(
            f"Unidades incompatibles: {from_unit} ({from_def.unit_type.value}) "
            f"no se puede convertir a {to_unit} ({to_def.unit_type.value})"
        )
    
    # Convertir a SI y luego a la unidad destino
    si_value = value * from_def.to_si
    result = si_value / to_def.to_si
    
    return result


def convert_to_si(value: float, unit: str) -> tuple[float, str]:
    """
    Convertir un valor a su unidad SI
    
    Args:
        value: Valor numérico
        unit: Código de la unidad
    
    Returns:
        Tupla (valor_en_si, unidad_si)
    """
    unit_def = get_unit(unit)
    si_value = value * unit_def.to_si
    return si_value, unit_def.si_unit


def format_value(value: float, unit: str, decimals: int = 3) -> str:
    """
    Formatear un valor con su símbolo de unidad
    
    Args:
        value: Valor numérico
        unit: Código de la unidad
        decimals: Número de decimales
    
    Returns:
        String formateado ej: "500.00 L/s"
    """
    unit_def = get_unit(unit)
    return f"{value:.{decimals}f} {unit_def.symbol}"


def get_units_by_type(unit_type: UnitType) -> Dict[str, UnitDefinition]:
    """Obtener todas las unidades de un tipo específico"""
    return {
        code: unit for code, unit in UNITS.items()
        if unit.unit_type == unit_type
    }


def list_available_units() -> Dict[str, list]:
    """Listar todas las unidades disponibles agrupadas por tipo"""
    result = {}
    for unit_type in UnitType:
        units = get_units_by_type(unit_type)
        result[unit_type.value] = [
            f"{code} ({unit.symbol})" for code, unit in units.items()
        ]
    return result


class UnitConverter:
    """Clase conversora de unidades con contexto"""
    
    def __init__(self):
        self.conversion_history = []
    
    def convert(self, value: float, from_unit: str, to_unit: str, 
                context: Optional[str] = None) -> float:
        """
        Convertir unidades con registro histórico
        
        Args:
            value: Valor a convertir
            from_unit: Unidad de origen
            to_unit: Unidad de destino
            context: Contexto opcional de la conversión
        
        Returns:
            Valor convertido
        """
        result = convert(value, from_unit, to_unit)
        
        self.conversion_history.append({
            'value': value,
            'from': from_unit,
            'to': to_unit,
            'result': result,
            'context': context
        })
        
        return result
    
    def get_history(self) -> list:
        """Obtener historial de conversiones"""
        return self.conversion_history.copy()
    
    def clear_history(self):
        """Limpiar historial de conversiones"""
        self.conversion_history = []


# Funciones utilitarias para casos comunes

def flow_convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convertir caudal"""
    return convert(value, from_unit, to_unit)


def volume_convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convertir volumen"""
    return convert(value, from_unit, to_unit)


def time_convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convertir tiempo"""
    return convert(value, from_unit, to_unit)


def concentration_convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convertir concentración"""
    return convert(value, from_unit, to_unit)


def power_convert(value: float, from_unit: str, to_unit: str) -> float:
    """Convertir potencia"""
    return convert(value, from_unit, to_unit)
