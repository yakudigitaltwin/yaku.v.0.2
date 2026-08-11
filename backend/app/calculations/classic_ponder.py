"""
Classic Ponder Calculation Module for PTAP (Water Treatment Plant)
Handles input value calculations and pondering for various PTAP variables
"""

import math
from typing import Dict, List, Optional, Union
from dataclasses import dataclass


@dataclass
class PonderResult:
    """Result of classic ponder calculations"""
    unit_id: str
    calculation_type: str
    ponder_value: float
    variables_used: Dict[str, float]
    formula: str
    validation_passed: bool
    warnings: List[str]


def validate_input_values(**kwargs) -> List[str]:
    """
    Validate input values for PTAP calculations.
    
    Args:
        **kwargs: Input parameters to validate
        
    Returns:
        List of validation warnings/errors
    """
    warnings = []
    
    # Validate flow rate
    if 'Q_m3_s' in kwargs:
        if kwargs['Q_m3_s'] <= 0:
            warnings.append("Flow rate (Q_m3_s) must be positive")
        elif kwargs['Q_m3_s'] > 10:
            warnings.append("Flow rate (Q_m3_s) seems unusually high (>10 m³/s)")
    
    # Validate volume
    if 'volume_m3' in kwargs:
        if kwargs['volume_m3'] <= 0:
            warnings.append("Volume must be positive")
        elif kwargs['volume_m3'] > 50000:
            warnings.append("Volume seems unusually high (>50,000 m³)")
    
    # Validate area
    if 'area_m2' in kwargs:
        if kwargs['area_m2'] <= 0:
            warnings.append("Area must be positive")
        elif kwargs['area_m2'] > 100000:
            warnings.append("Area seems unusually high (>100,000 m²)")
    
    # Validate depth
    if 'depth_m' in kwargs:
        if kwargs['depth_m'] <= 0:
            warnings.append("Depth must be positive")
        elif kwargs['depth_m'] > 20:
            warnings.append("Depth seems unusually high (>20 m)")
    
    # Validate velocity gradients
    if 'G_s' in kwargs:
        if kwargs['G_s'] <= 0:
            warnings.append("Velocity gradient (G_s) must be positive")
        elif kwargs['G_s'] > 1000:
            warnings.append("Velocity gradient (G_s) seems unusually high (>1000 s⁻¹)")
    
    # Validate chemical dosages
    if 'coagulant_mg_l' in kwargs:
        if kwargs['coagulant_mg_l'] < 0:
            warnings.append("Coagulant dosage cannot be negative")
        elif kwargs['coagulant_mg_l'] > 200:
            warnings.append("Coagulant dosage seems unusually high (>200 mg/L)")
    
    if 'chlorine_mg_l' in kwargs:
        if kwargs['chlorine_mg_l'] < 0:
            warnings.append("Chlorine dosage cannot be negative")
        elif kwargs['chlorine_mg_l'] > 10:
            warnings.append("Chlorine dosage seems unusually high (>10 mg/L)")
    
    # Validate turbidity
    if 'turbidity_ntu' in kwargs:
        if kwargs['turbidity_ntu'] < 0:
            warnings.append("Turbidity cannot be negative")
        elif kwargs['turbidity_ntu'] > 1000:
            warnings.append("Turbidity seems unusually high (>1000 NTU)")
    
    # Validate pH
    if 'pH' in kwargs:
        if kwargs['pH'] < 0 or kwargs['pH'] > 14:
            warnings.append("pH must be between 0 and 14")
    
    return warnings


def calculate_hydraulic_loading_rate(Q_m3_s: float, area_m2: float) -> float:
    """
    Calculate hydraulic loading rate for sedimentation units.
    
    Args:
        Q_m3_s: Flow rate in m³/s
        area_m2: Surface area in m²
        
    Returns:
        Hydraulic loading rate in m³/m²/day
    """
    if Q_m3_s <= 0 or area_m2 <= 0:
        raise ValueError("Flow rate and area must be positive")
    
    return (Q_m3_s * 86400) / area_m2


def calculate_surface_overflow_rate(Q_m3_s: float, area_m2: float) -> float:
    """
    Calculate surface overflow rate for sedimentation units.
    
    Args:
        Q_m3_s: Flow rate in m³/s
        area_m2: Surface area in m²
        
    Returns:
        Surface overflow rate in m³/m²/h
    """
    if Q_m3_s <= 0 or area_m2 <= 0:
        raise ValueError("Flow rate and area must be positive")
    
    return (Q_m3_s * 3600) / area_m2


def calculate_detention_time(volume_m3: float, Q_m3_s: float) -> float:
    """
    Calculate detention time for process units.
    
    Args:
        volume_m3: Volume in m³
        Q_m3_s: Flow rate in m³/s
        
    Returns:
        Detention time in hours
    """
    if volume_m3 <= 0 or Q_m3_s <= 0:
        raise ValueError("Volume and flow rate must be positive")
    
    return volume_m3 / Q_m3_s / 3600


def calculate_mixing_energy(G_s: float, volume_m3: float, mu_pa_s: float = 0.001) -> float:
    """
    Calculate mixing energy required for rapid mix units.
    
    Args:
        G_s: Velocity gradient in s⁻¹
        volume_m3: Volume in m³
        mu_pa_s: Dynamic viscosity in Pa·s (default 0.001 for water at 20°C)
        
    Returns:
        Power requirement in watts
    """
    if G_s <= 0 or volume_m3 <= 0 or mu_pa_s <= 0:
        raise ValueError("G_s, volume, and viscosity must be positive")
    
    return mu_pa_s * (G_s ** 2) * volume_m3


def calculate_floculation_efficiency(G_s: float, detention_time_h: float) -> float:
    """
    Calculate floculation efficiency based on Gt value.
    
    Args:
        G_s: Velocity gradient in s⁻¹
        detention_time_h: Detention time in hours
        
    Returns:
        Gt value (dimensionless)
    """
    if G_s <= 0 or detention_time_h <= 0:
        raise ValueError("G_s and detention time must be positive")
    
    return G_s * detention_time_h * 3600


def calculate_filtration_rate(Q_m3_s: float, area_m2: float) -> float:
    """
    Calculate filtration rate for filtration units.
    
    Args:
        Q_m3_s: Flow rate in m³/s
        area_m2: Filter area in m²
        
    Returns:
        Filtration rate in m³/m²/h
    """
    if Q_m3_s <= 0 or area_m2 <= 0:
        raise ValueError("Flow rate and area must be positive")
    
    return (Q_m3_s * 3600) / area_m2


def calculate_disinfection_contact_time(volume_m3: float, Q_m3_s: float) -> float:
    """
    Calculate contact time for disinfection units.
    
    Args:
        volume_m3: Disinfection chamber volume in m³
        Q_m3_s: Flow rate in m³/s
        
    Returns:
        Contact time in minutes
    """
    if volume_m3 <= 0 or Q_m3_s <= 0:
        raise ValueError("Volume and flow rate must be positive")
    
    return (volume_m3 / Q_m3_s) / 60


def calculate_CT_value(chlorine_mg_l: float, contact_time_min: float) -> float:
    """
    Calculate CT value for disinfection.
    
    Args:
        chlorine_mg_l: Chlorine concentration in mg/L
        contact_time_min: Contact time in minutes
        
    Returns:
        CT value in mg·min/L
    """
    if chlorine_mg_l < 0 or contact_time_min <= 0:
        raise ValueError("Chlorine dosage must be non-negative and contact time must be positive")
    
    return chlorine_mg_l * contact_time_min


def calculate_unit_efficiency(unit_type: str, parameters: Dict[str, float]) -> Dict[str, float]:
    """
    Calculate efficiency scores for different unit types.
    
    Args:
        unit_type: Type of process unit
        parameters: Unit parameters
        
    Returns:
        Dictionary with efficiency metrics
    """
    efficiency_metrics = {}
    
    if unit_type == "sedimentation":
        area_m2 = parameters.get("area_m2", 1500)
        Q_m3_s = parameters.get("Q_m3_s", 0.5)
        surface_overflow = calculate_surface_overflow_rate(Q_m3_s, area_m2)
        
        # Efficiency based on surface overflow rate (lower is better)
        efficiency_metrics["surface_overflow_rate_m_h"] = surface_overflow
        efficiency_metrics["efficiency_score"] = max(0, 100 - surface_overflow * 10)
        efficiency_metrics["turbidity_removal_percent"] = 65  # Typical value
        
    elif unit_type == "filtration":
        area_m2 = parameters.get("area_m2", 250)
        Q_m3_s = parameters.get("Q_m3_s", 0.5)
        filtration_rate = calculate_filtration_rate(Q_m3_s, area_m2)
        
        # Efficiency based on filtration rate (optimal range 5-15 m³/m²/h)
        if 5 <= filtration_rate <= 15:
            efficiency_metrics["efficiency_score"] = 100
        elif filtration_rate < 5:
            efficiency_metrics["efficiency_score"] = 80
        else:
            efficiency_metrics["efficiency_score"] = max(0, 100 - (filtration_rate - 15) * 5)
        
        efficiency_metrics["filtration_rate_m_h"] = filtration_rate
        efficiency_metrics["turbidity_removal_percent"] = 85  # Typical value
        
    elif unit_type == "disinfection":
        chlorine_mg_l = parameters.get("chlorine_mg_l", 1.5)
        contact_time_min = parameters.get("contact_time_min", 15)
        CT_value = calculate_CT_value(chlorine_mg_l, contact_time_min)
        
        # Efficiency based on CT value for virus inactivation
        if CT_value >= 120:  # 4-log inactivation for viruses
            efficiency_metrics["efficiency_score"] = 100
        elif CT_value >= 60:  # 2-log inactivation
            efficiency_metrics["efficiency_score"] = 80
        else:
            efficiency_metrics["efficiency_score"] = min(80, CT_value / 60 * 80)
        
        efficiency_metrics["CT_value_mg_min_l"] = CT_value
        efficiency_metrics["log_inactivation"] = min(6, CT_value / 20)  # Simplified calculation
        
    elif unit_type == "rapid_mix":
        G_s = parameters.get("G_s", 60)
        volume_m3 = parameters.get("volume_m3", 30)
        Q_m3_s = parameters.get("Q_m3_s", 0.5)
        
        detention_time = detention_time(volume_m3, Q_m3_s)
        mixing_energy = calculate_mixing_energy(G_s, volume_m3)
        
        # Efficiency based on G value (optimal 500-1000 s⁻¹)
        if 500 <= G_s <= 1000:
            efficiency_metrics["efficiency_score"] = 100
        elif G_s < 500:
            efficiency_metrics["efficiency_score"] = min(100, G_s / 500 * 100)
        else:
            efficiency_metrics["efficiency_score"] = max(0, 100 - (G_s - 1000) / 100 * 20)
        
        efficiency_metrics["G_s"] = G_s
        efficiency_metrics["detention_time_min"] = detention_time * 60
        efficiency_metrics["power_w"] = mixing_energy
        
    elif unit_type == "flocculation":
        G_s = parameters.get("G_s", 30)
        volume_m3 = parameters.get("volume_m3", 750)
        Q_m3_s = parameters.get("Q_m3_s", 0.5)
        
        detention_time = detention_time(volume_m3, Q_m3_s)
        Gt_value = calculate_floculation_efficiency(G_s, detention_time)
        
        # Efficiency based on Gt value (optimal 20,000-100,000)
        if 20000 <= Gt_value <= 100000:
            efficiency_metrics["efficiency_score"] = 100
        elif Gt_value < 20000:
            efficiency_metrics["efficiency_score"] = min(100, Gt_value / 20000 * 100)
        else:
            efficiency_metrics["efficiency_score"] = max(0, 100 - (Gt_value - 100000) / 100000 * 50)
        
        efficiency_metrics["G_s"] = G_s
        efficiency_metrics["Gt_value"] = Gt_value
        efficiency_metrics["detention_time_min"] = detention_time * 60
    
    return efficiency_metrics


def classic_ponder_calculation(unit_type: str, parameters: Dict[str, float], 
                              calculation_type: str = "design") -> PonderResult:
    """
    Perform classic ponder calculation for PTAP units.
    
    Args:
        unit_type: Type of process unit
        parameters: Dictionary of unit parameters
        calculation_type: "design", "performance", or "efficiency"
        
    Returns:
        PonderResult object with calculation results
    """
    # Validate input values
    warnings = validate_input_values(**parameters)
    validation_passed = len(warnings) == 0
    
    try:
        if calculation_type == "design":
            # Design calculations
            if unit_type == "rapid_mix":
                Q_m3_s = parameters.get("Q_m3_s", 0.5)
                volume_m3 = parameters.get("volume_m3", 30)
                G_s = parameters.get("G_s", 60)
                
                results = {
                    "detention_time_s": volume_m3 / Q_m3_s,
                    "detention_time_min": (volume_m3 / Q_m3_s) / 60,
                    "power_w": calculate_mixing_energy(G_s, volume_m3),
                    "formula": "t = V/Q, P = μ·G²·V"
                }
                
            elif unit_type == "flocculation":
                Q_m3_s = parameters.get("Q_m3_s", 0.5)
                volume_m3 = parameters.get("volume_m3", 750)
                G_s = parameters.get("G_s", 30)
                
                detention_time_h = calculate_detention_time(volume_m3, Q_m3_s)
                Gt_value = calculate_floculation_efficiency(G_s, detention_time_h)
                
                results = {
                    "detention_time_s": volume_m3 / Q_m3_s,
                    "detention_time_min": (volume_m3 / Q_m3_s) / 60,
                    "detention_time_h": detention_time_h,
                    "Gt_value": Gt_value,
                    "formula": "t = V/Q, Gt = G·t·3600"
                }
                
            elif unit_type == "sedimentation":
                Q_m3_s = parameters.get("Q_m3_s", 0.5)
                area_m2 = parameters.get("area_m2", 1500)
                depth_m = parameters.get("depth_m", 4)
                
                volume = area_m2 * depth_m
                surface_overflow = calculate_surface_overflow_rate(Q_m3_s, area_m2)
                hydraulic_loading = calculate_hydraulic_loading_rate(Q_m3_s, area_m2)
                detention_time_h = calculate_detention_time(volume, Q_m3_s)
                
                results = {
                    "surface_overflow_rate_m_h": surface_overflow,
                    "hydraulic_loading_rate_m3_m2_day": hydraulic_loading,
                    "volume_m3": volume,
                    "detention_time_h": detention_time_h,
                    "depth_m": depth_m,
                    "formula": "V = A·h, SOR = Q/A·3600, HLR = Q/A·86400"
                }
                
            elif unit_type == "filtration":
                Q_m3_s = parameters.get("Q_m3_s", 0.5)
                area_m2 = parameters.get("area_m2", 250)
                
                filtration_rate = calculate_filtration_rate(Q_m3_s, area_m2)
                
                results = {
                    "filtration_rate_m_h": filtration_rate,
                    "formula": "FR = Q/A·3600"
                }
                
            elif unit_type == "disinfection":
                Q_m3_s = parameters.get("Q_m3_s", 0.5)
                volume_m3 = parameters.get("volume_m3", 900)
                chlorine_mg_l = parameters.get("chlorine_mg_l", 1.5)
                
                contact_time_min = calculate_disinfection_contact_time(volume_m3, Q_m3_s)
                CT_value = calculate_CT_value(chlorine_mg_l, contact_time_min)
                
                results = {
                    "contact_time_min": contact_time_min,
                    "CT_value_mg_min_l": CT_value,
                    "formula": "t = V/Q, CT = C·t"
                }
                
            else:
                raise ValueError(f"Unsupported unit type for design calculation: {unit_type}")
            
            ponder_value = sum(results.values()) / len(results) if results else 0
            
        elif calculation_type == "performance":
            # Performance calculations
            if unit_type in ["sedimentation", "filtration", "disinfection"]:
                results = calculate_unit_efficiency(unit_type, parameters)
                ponder_value = results.get("efficiency_score", 0)
                formula = "Efficiency based on operational parameters"
            else:
                raise ValueError(f"Performance calculation not supported for unit type: {unit_type}")
                
        elif calculation_type == "efficiency":
            # Efficiency calculations
            results = calculate_unit_efficiency(unit_type, parameters)
            ponder_value = results.get("efficiency_score", 0)
            formula = "Efficiency scoring based on industry standards"
            
        else:
            raise ValueError(f"Unsupported calculation type: {calculation_type}")
        
        return PonderResult(
            unit_id=parameters.get("id", "unknown"),
            calculation_type=calculation_type,
            ponder_value=ponder_value,
            variables_used=parameters,
            formula=formula,
            validation_passed=validation_passed,
            warnings=warnings
        )
        
    except Exception as e:
        return PonderResult(
            unit_id=parameters.get("id", "unknown"),
            calculation_type=calculation_type,
            ponder_value=0,
            variables_used=parameters,
            formula="Calculation failed",
            validation_passed=False,
            warnings=warnings + [f"Calculation error: {str(e)}"]
        )