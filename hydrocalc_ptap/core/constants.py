"""
Constantes físicas y parámetros de diseño para HYDROCALC-PTAP

Incluye:
- Constantes físicas del agua
- Parámetros típicos de diseño PTAP
- Rangos recomendados por normativa
- Propiedades de químicos comunes
"""

from dataclasses import dataclass
from typing import Dict, List, Optional


# ============================================================================
# CONSTANTES FÍSICAS DEL AGUA
# ============================================================================

@dataclass
class WaterProperties:
    """Propiedades físicas del agua a diferentes temperaturas"""
    temperature: float  # °C
    density: float  # kg/m³
    viscosity_dynamic: float  # Pa·s
    viscosity_kinematic: float  # m²/s
    surface_tension: float  # N/m
    
WATER_PROPERTIES: Dict[float, WaterProperties] = {
    0: WaterProperties(0, 999.84, 1.792e-3, 1.792e-6, 0.0756),
    5: WaterProperties(5, 999.96, 1.519e-3, 1.519e-6, 0.0749),
    10: WaterProperties(10, 999.70, 1.307e-3, 1.307e-6, 0.0742),
    15: WaterProperties(15, 999.10, 1.138e-3, 1.139e-6, 0.0735),
    20: WaterProperties(20, 998.21, 1.002e-3, 1.004e-6, 0.0728),
    25: WaterProperties(25, 997.05, 0.890e-3, 0.893e-6, 0.0720),
    30: WaterProperties(30, 995.65, 0.798e-3, 0.801e-6, 0.0712),
    35: WaterProperties(35, 994.04, 0.720e-3, 0.724e-6, 0.0704),
    40: WaterProperties(40, 992.22, 0.653e-3, 0.658e-6, 0.0696),
}

# Valores por defecto (20°C)
DEFAULT_WATER_TEMP = 20.0
DEFAULT_WATER_DENSITY = 998.21  # kg/m³
DEFAULT_WATER_VISCOSITY = 1.002e-3  # Pa·s
DEFAULT_GRAVITY = 9.80665  # m/s²


def get_water_properties(temperature: float) -> WaterProperties:
    """
    Obtener propiedades del agua para una temperatura dada
    Usa interpolación lineal si la temperatura no está en la tabla
    """
    temps = sorted(WATER_PROPERTIES.keys())
    
    # Si está exactamente en la tabla
    if temperature in WATER_PROPERTIES:
        return WATER_PROPERTIES[temperature]
    
    # Si está fuera de rango
    if temperature < temps[0]:
        return WATER_PROPERTIES[temps[0]]
    if temperature > temps[-1]:
        return WATER_PROPERTIES[temps[-1]]
    
    # Interpolación lineal
    for i in range(len(temps) - 1):
        if temps[i] <= temperature <= temps[i + 1]:
            t1, t2 = temps[i], temps[i + 1]
            p1, p2 = WATER_PROPERTIES[t1], WATER_PROPERTIES[t2]
            
            # Factor de interpolación
            f = (temperature - t1) / (t2 - t1)
            
            return WaterProperties(
                temperature=temperature,
                density=p1.density + f * (p2.density - p1.density),
                viscosity_dynamic=p1.viscosity_dynamic + f * (p2.viscosity_dynamic - p1.viscosity_dynamic),
                viscosity_kinematic=p1.viscosity_kinematic + f * (p2.viscosity_kinematic - p1.viscosity_kinematic),
                surface_tension=p1.surface_tension + f * (p2.surface_tension - p1.surface_tension),
            )
    
    return WATER_PROPERTIES[DEFAULT_WATER_TEMP]


# ============================================================================
# PARÁMETROS DE DISEÑO PTAP
# ============================================================================

@dataclass
class DesignParameter:
    """Parámetro de diseño con rango recomendado"""
    name: str
    symbol: str
    unit: str
    min_value: float
    max_value: float
    typical_value: float
    description: str
    reference: str = ""


# Parámetros de mezcla rápida
RAPID_MIXING_PARAMS = {
    'G': DesignParameter(
        "Gradiente de velocidad", "G", "s⁻¹",
        300, 1000, 600,
        "Gradiente de velocidad para mezcla rápida",
        "AWWA, ASCE"
    ),
    'T': DesignParameter(
        "Tiempo de mezcla", "T", "s",
        10, 60, 30,
        "Tiempo de retención en mezcla rápida",
        "AWWA, ASCE"
    ),
    'GT': DesignParameter(
        "Número de Camp", "GT", "adimensional",
        10000, 60000, 30000,
        "Producto G×T para mezcla rápida",
        "Camp & Stein"
    ),
}

# Parámetros de floculación
FLOCCULATION_PARAMS = {
    'G': DesignParameter(
        "Gradiente de velocidad", "G", "s⁻¹",
        20, 80, 50,
        "Gradiente de velocidad para floculación",
        "AWWA, ASCE"
    ),
    'T': DesignParameter(
        "Tiempo de floculación", "T", "min",
        15, 45, 30,
        "Tiempo de retención hidráulica",
        "AWWA, ASCE"
    ),
    'GT': DesignParameter(
        "Número de Camp", "GT", "adimensional",
        20000, 200000, 100000,
        "Producto G×T para floculación",
        "Camp & Stein"
    ),
    'v': DesignParameter(
        "Velocidad del flujo", "v", "m/s",
        0.1, 0.3, 0.2,
        "Velocidad del agua en floculador",
        "AWWA"
    ),
}

# Parámetros de sedimentación
SEDIMENTATION_PARAMS = {
    'q': DesignParameter(
        "Carga superficial", "q", "m³/m²·d",
        20, 60, 40,
        "Tasa de desborde en sedimentador",
        "AWWA, ASCE"
    ),
    'T': DesignParameter(
        "Tiempo de retención", "T", "h",
        2, 6, 4,
        "Tiempo de retención hidráulica",
        "AWWA, ASCE"
    ),
    'v': DesignParameter(
        "Velocidad horizontal", "v", "m/min",
        0.3, 1.0, 0.6,
        "Velocidad horizontal del flujo",
        "AWWA"
    ),
    'L_H': DesignParameter(
        "Relación largo/ancho", "L/H", "adimensional",
        3, 6, 4,
        "Relación geométrica del tanque",
        "AWWA"
    ),
}

# Parámetros de filtración
FILTRATION_PARAMS = {
    'v_f': DesignParameter(
        "Velocidad de filtración", "v_f", "m/h",
        4, 8, 6,
        "Tasa de filtración",
        "AWWA, ASCE"
    ),
    'T_f': DesignParameter(
        "Tiempo de filtro", "T_f", "h",
        24, 72, 48,
        "Tiempo entre lavados",
        "AWWA"
    ),
    'v_lav': DesignParameter(
        "Velocidad de lavado", "v_lav", "m/h",
        30, 60, 45,
        "Tasa de lavado del filtro",
        "AWWA"
    ),
    'expansion': DesignParameter(
        "Expansión del lecho", "exp", "%",
        20, 40, 30,
        "Expansión del medio filtrante durante lavado",
        "AWWA"
    ),
}

# Parámetros de desinfección
DISINFECTION_PARAMS = {
    'CT': DesignParameter(
        "Valor CT", "CT", "mg·min/L",
        15, 100, 30,
        "Concentración × Tiempo para cloro",
        "EPA, WHO"
    ),
    'Cl_res': DesignParameter(
        "Cloro residual", "Cl_res", "mg/L",
        0.2, 0.5, 0.3,
        "Cloro residual libre en red",
        "WHO, EPA"
    ),
    'T_contact': DesignParameter(
        "Tiempo de contacto", "T", "min",
        20, 60, 30,
        "Tiempo de contacto mínimo",
        "EPA, WHO"
    ),
}


def get_design_parameter(category: str, param: str) -> Optional[DesignParameter]:
    """Obtener parámetro de diseño por categoría y nombre"""
    categories = {
        'rapid_mixing': RAPID_MIXING_PARAMS,
        'flocculation': FLOCCULATION_PARAMS,
        'sedimentation': SEDIMENTATION_PARAMS,
        'filtration': FILTRATION_PARAMS,
        'disinfection': DISINFECTION_PARAMS,
    }
    
    if category not in categories:
        raise ValueError(f"Categoría desconocida: {category}")
    
    params = categories[category]
    return params.get(param)


def check_parameter_range(category: str, param: str, value: float) -> dict:
    """
    Verificar si un valor está dentro del rango recomendado
    
    Returns:
        Dict con:
        - in_range: bool
        - warning: str o None
        - parameter: DesignParameter
    """
    parameter = get_design_parameter(category, param)
    
    if parameter is None:
        return {
            'in_range': False,
            'warning': f"Parámetro '{param}' no encontrado en categoría '{category}'",
            'parameter': None
        }
    
    in_range = parameter.min_value <= value <= parameter.max_value
    
    if not in_range:
        if value < parameter.min_value:
            warning = (f"{value} {parameter.unit} está por debajo del mínimo recomendado "
                      f"({parameter.min_value} {parameter.unit})")
        else:
            warning = (f"{value} {parameter.unit} está por encima del máximo recomendado "
                      f"({parameter.max_value} {parameter.unit})")
    else:
        warning = None
    
    return {
        'in_range': in_range,
        'warning': warning,
        'parameter': parameter
    }


# ============================================================================
# PROPIEDADES DE QUÍMICOS
# ============================================================================

@dataclass
class Chemical:
    """Propiedades de un químico para tratamiento de agua"""
    name: str
    formula: str
    molecular_weight: float  # g/mol
    purity_typical: float  # % (0-100)
    density: float  # kg/m³ o g/mL para líquidos
    state: str  # 'solid', 'liquid', 'gas'
    dosage_range: tuple  # (min, max) mg/L
    application: str
    hazards: List[str]


CHEMICALS: Dict[str, Chemical] = {
    # Coagulantes
    'alum': Chemical(
        "Sulfato de aluminio", "Al₂(SO₄)₃·14H₂O",
        594.19, 98.0, 1000, 'solid',
        (5, 100), "Coagulación",
        ["Irritante", "No incompatible con bases fuertes"]
    ),
    'pac': Chemical(
        "Cloruro de polialuminio", "[Al₂(OH)ₙCl₆₋ₙ]ₘ",
        174.45, 90.0, 1200, 'liquid',
        (1, 50), "Coagulación",
        ["Corrosivo", "Manejar con protección"]
    ),
    'ferric_chloride': Chemical(
        "Cloruro férrico", "FeCl₃",
        162.20, 95.0, 1400, 'solid',
        (5, 80), "Coagulación",
        ["Corrosivo", "Higroscópico"]
    ),
    'ferric_sulfate': Chemical(
        "Sulfato férrico", "Fe₂(SO₄)₃",
        399.88, 96.0, 1100, 'solid',
        (5, 80), "Coagulación",
        ["Irritante", "Higroscópico"]
    ),
    
    # Ayudantes de coagulación
    'polyelectrolyte': Chemical(
        "Polielectrolito", "(C₃H₅NO)ₙ",
        100000, 99.0, 500, 'liquid',
        (0.1, 2), "Ayudante de coagulación",
        ["Manejar con cuidado", "Evitar inhalación"]
    ),
    
    # Ajuste de pH
    'lime': Chemical(
        "Cal hidratada", "Ca(OH)₂",
        74.09, 95.0, 2200, 'solid',
        (10, 200), "Ajuste de pH y alcalinidad",
        ["Corrosivo", "Irritante severo"]
    ),
    'soda_ash': Chemical(
        "Carbonato de sodio", "Na₂CO₃",
        105.99, 99.0, 2540, 'solid',
        (10, 150), "Ajuste de pH y alcalinidad",
        ["Irritante", "Higroscópico"]
    ),
    'caustic_soda': Chemical(
        "Hidróxido de sodio", "NaOH",
        40.00, 98.0, 2130, 'solid',
        (5, 100), "Ajuste de pH",
        ["Corrosivo severo", "Exotérmico en agua"]
    ),
    'co2': Chemical(
        "Dióxido de carbono", "CO₂",
        44.01, 99.5, 1.98, 'gas',
        (5, 50), "Recarbonatación",
        ["Asfixiante en altas concentraciones"]
    ),
    
    # Desinfectantes
    'chlorine_gas': Chemical(
        "Cloro gas", "Cl₂",
        70.90, 99.5, 3.2, 'gas',
        (0.5, 5), "Desinfección",
        ["Tóxico", "Oxidante fuerte", "Peligroso"]
    ),
    'sodium_hypochlorite': Chemical(
        "Hipoclorito de sodio", "NaOCl",
        74.44, 12.0, 1200, 'liquid',
        (1, 10), "Desinfección",
        ["Corrosivo", "Oxidante", "Incompatible con ácidos"]
    ),
    'calcium_hypochlorite': Chemical(
        "Hipoclorito de calcio", "Ca(OCl)₂",
        142.98, 65.0, 2350, 'solid',
        (1, 10), "Desinfección",
        ["Oxidante fuerte", "Incompatible con orgánicos"]
    ),
    'chlorine_dioxide': Chemical(
        "Dióxido de cloro", "ClO₂",
        67.45, 98.0, 3.0, 'gas',
        (0.1, 2), "Desinfección",
        ["Explosivo", "Tóxico", "Inestable"]
    ),
    'ozone': Chemical(
        "Ozono", "O₃",
        48.00, 95.0, 2.1, 'gas',
        (0.5, 5), "Desinfección y oxidación",
        ["Tóxico", "Oxidante muy fuerte", "Inestable"]
    ),
    
    # Fluoración
    'sodium_fluoride': Chemical(
        "Fluoruro de sodio", "NaF",
        41.99, 98.0, 2790, 'solid',
        (0.5, 1.5), "Fluoración",
        ["Tóxico en altas dosis"]
    ),
    'fluorosilicic_acid': Chemical(
        "Ácido fluorosilícico", "H₂SiF₆",
        144.09, 25.0, 1380, 'liquid',
        (0.5, 1.5), "Fluoración",
        ["Corrosivo", "Tóxico"]
    ),
}


def get_chemical(name: str) -> Optional[Chemical]:
    """Obtener información de un químico por nombre"""
    return CHEMICALS.get(name.lower())


def list_chemicals(application: Optional[str] = None) -> List[str]:
    """Listar químicos disponibles, opcionalmente filtrados por aplicación"""
    if application is None:
        return list(CHEMICALS.keys())
    
    return [
        name for name, chem in CHEMICALS.items()
        if application.lower() in chem.application.lower()
    ]


def calculate_dosage_mass(flow: float, dose: float, 
                          chemical_name: str, purity: Optional[float] = None) -> float:
    """
    Calcular masa diaria de químico requerida
    
    Args:
        flow: Caudal en m³/día
        dose: Dosis en mg/L
        chemical_name: Nombre del químico
        purity: Pureza específica (si None, usa la típica)
    
    Returns:
        Masa diaria en kg/día
    """
    chemical = get_chemical(chemical_name)
    if chemical is None:
        raise ValueError(f"Químico desconocido: {chemical_name}")
    
    if purity is None:
        purity = chemical.purity_typical
    
    # Fórmula: Masa (kg/d) = Q (m³/d) × Dosis (mg/L) / (Pureza × 1000)
    mass_per_day = (flow * dose) / (purity / 100 * 1000)
    
    return mass_per_day
