import numpy as np
from app.domain.plant import PlantModel
from app.domain.process_unit import ProcessUnit
from app.domain.stream import Stream
from app.calculations.design import design_plant, rapid_mix, flocculation, sedimentation, filtration, disinfection

def build_demo_plant():
    q = 0.5
    units = [
        ProcessUnit(id="raw_water", type="source", name="Agua cruda",
                    parameters={"Q_m3_s": q, "turbidity_ntu": 20, "pH": 7.2}),
        ProcessUnit(id="rapid_mix", type="rapid_mix", name="Mezcla rápida / coagulación",
                    parameters={"Q_m3_s": q, "volume_m3": 30, "G_s": 60,
                                "coagulant_mg_l": 25}),
        ProcessUnit(id="flocculation", type="flocculation", name="Floculación",
                    parameters={"Q_m3_s": q, "volume_m3": 750, "G_s": 30}),
        ProcessUnit(id="sedimentation", type="sedimentation", name="Sedimentación",
                    parameters={"Q_m3_s": q, "area_m2": 1500, "depth_m": 4}),
        ProcessUnit(id="filtration", type="filtration", name="Filtración",
                    parameters={"Q_m3_s": q, "area_m2": 250, "headloss_m": 2}),
        ProcessUnit(id="disinfection", type="disinfection", name="Desinfección",
                    parameters={"Q_m3_s": q, "volume_m3": 900, "chlorine_mg_l": 1.5}),
        ProcessUnit(id="treated_water", type="sink", name="Agua tratada")
    ]
    streams = [
        Stream(id="s1", source="raw_water", target="rapid_mix", flow_m3_s=q),
        Stream(id="s2", source="rapid_mix", target="flocculation", flow_m3_s=q),
        Stream(id="s3", source="flocculation", target="sedimentation", flow_m3_s=q),
        Stream(id="s4", source="sedimentation", target="filtration", flow_m3_s=q),
        Stream(id="s5", source="filtration", target="disinfection", flow_m3_s=q),
        Stream(id="s6", source="disinfection", target="treated_water", flow_m3_s=q),
    ]
    return PlantModel(id="ptap-demo", name="Yaku PTAP Demo — 500 L/s",
                      units=units, streams=streams,
                      metadata={"version": "0.1", "purpose": "demo"})

def simulate_plant(plant, duration_s, dt_s):
    if dt_s > duration_s:
        raise ValueError("dt_s no puede superar duration_s")
    raw_turb = plant.get_unit("raw_water").parameter("turbidity_ntu", 20)
    chlorine = plant.get_unit("disinfection").parameter("chlorine_mg_l", 1.5)
    target_turb = raw_turb * 0.70 * 0.65 * 0.85
    tau = 300.0
    k = 0.002 / 60.0
    turb = raw_turb
    states = []
    for ti in np.arange(0, duration_s + dt_s, dt_s):
        turb += dt_s * (target_turb - turb) / tau
        cl = chlorine * np.exp(-k * ti)
        states.append({
            "time_s": float(ti),
            "turbidity_ntu": float(turb),
            "chlorine_mg_l": float(cl)
        })
    return {
        "plant_id": plant.id,
        "duration_s": duration_s,
        "dt_s": dt_s,
        "states": states,
        "model_note": "Modelo agregado demostrativo; requiere calibración y validación."
    }

def calculate_unit(unit_type: str, parameters: dict[str, float], calculation_type: str = "design"):
    """
    Calculate design or performance parameters for a specific process unit type.
    
    Args:
        unit_type: Type of process unit (rapid_mix, flocculation, sedimentation, filtration, disinfection)
        parameters: Dictionary of unit parameters
        calculation_type: "design" or "performance"
    
    Returns:
        Dictionary with calculation results
    """
    if calculation_type == "design":
        if unit_type == "rapid_mix":
            return rapid_mix(
                parameters.get("Q_m3_s", 0.5),
                parameters.get("volume_m3", 30),
                parameters.get("G_s", 60)
            )
        elif unit_type == "flocculation":
            return flocculation(
                parameters.get("Q_m3_s", 0.5),
                parameters.get("volume_m3", 750),
                parameters.get("G_s", 30)
            )
        elif unit_type == "sedimentation":
            return sedimentation(
                parameters.get("Q_m3_s", 0.5),
                parameters.get("area_m2", 1500),
                parameters.get("depth_m", 4)
            )
        elif unit_type == "filtration":
            return filtration(
                parameters.get("Q_m3_s", 0.5),
                parameters.get("area_m2", 250)
            )
        elif unit_type == "disinfection":
            return disinfection(
                parameters.get("Q_m3_s", 0.5),
                parameters.get("volume_m3", 900),
                parameters.get("chlorine_mg_l", 1.5)
            )
        else:
            raise ValueError(f"Unsupported unit type for design calculation: {unit_type}")
    
    elif calculation_type == "performance":
        # Performance calculations could include efficiency, removal rates, etc.
        if unit_type == "sedimentation":
            turbidity_removal = 0.65  # 65% turbidity removal
            area_m2 = parameters.get("area_m2", 1500)
            Q_m3_s = parameters.get("Q_m3_s", 0.5)
            surface_overflow = Q_m3_s / area_m2
            return {
                "turbidity_removal_percent": turbidity_removal * 100,
                "surface_overflow_rate_m_h": surface_overflow * 3600,
                "efficiency_score": min(100, surface_overflow * 1000)  # Simplified efficiency
            }
        elif unit_type == "filtration":
            turbidity_removal = 0.85  # 85% turbidity removal
            area_m2 = parameters.get("area_m2", 250)
            Q_m3_s = parameters.get("Q_m3_s", 0.5)
            filtration_rate = Q_m3_s / area_m2
            return {
                "turbidity_removal_percent": turbidity_removal * 100,
                "filtration_rate_m_h": filtration_rate * 3600,
                "efficiency_score": min(100, filtration_rate * 2000)  # Simplified efficiency
            }
        elif unit_type == "disinfection":
            chlorine_mg_l = parameters.get("chlorine_mg_l", 1.5)
            contact_time_min = parameters.get("contact_time_min", 15)
            CT_value = chlorine_mg_l * contact_time_min
            return {
                "CT_value_mg_min_l": CT_value,
                "log_inactivation": min(6, CT_value / 10),  # Simplified CT-based inactivation
                "efficiency_score": min(100, CT_value * 5)  # Simplified efficiency
            }
        else:
            raise ValueError(f"Performance calculation not supported for unit type: {unit_type}")
    
    else:
        raise ValueError(f"Unsupported calculation type: {calculation_type}")
