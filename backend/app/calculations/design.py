from app.domain.plant import PlantModel

def rapid_mix(Q_m3_s, volume_m3, G_s, mu_pa_s=0.001):
    if Q_m3_s <= 0 or volume_m3 <= 0:
        raise ValueError("Q y volumen deben ser positivos")
    t = volume_m3 / Q_m3_s
    power = mu_pa_s * G_s**2 * volume_m3
    return {"detention_time_s": t, "detention_time_min": t/60, "power_w": power}

def flocculation(Q_m3_s, volume_m3, G_s):
    if Q_m3_s <= 0 or volume_m3 <= 0:
        raise ValueError("Q y volumen deben ser positivos")
    t = volume_m3 / Q_m3_s
    return {"detention_time_s": t, "detention_time_min": t/60, "Gt": G_s*t}

def sedimentation(Q_m3_s, area_m2, depth_m):
    if Q_m3_s <= 0 or area_m2 <= 0 or depth_m <= 0:
        raise ValueError("Q, área y profundidad deben ser positivos")
    volume = area_m2 * depth_m
    return {
        "surface_overflow_m_s": Q_m3_s / area_m2,
        "surface_overflow_m_h": Q_m3_s / area_m2 * 3600,
        "volume_m3": volume,
        "detention_time_h": volume / Q_m3_s / 3600
    }

def filtration(Q_m3_s, area_m2):
    if Q_m3_s <= 0 or area_m2 <= 0:
        raise ValueError("Q y área deben ser positivos")
    return {"filtration_rate_m_h": Q_m3_s / area_m2 * 3600}

def disinfection(Q_m3_s, volume_m3, chlorine_mg_l):
    if Q_m3_s <= 0 or volume_m3 <= 0:
        raise ValueError("Q y volumen deben ser positivos")
    t_min = volume_m3 / Q_m3_s / 60
    return {"contact_time_min": t_min, "CT_mg_min_l": chlorine_mg_l*t_min}

def design_plant(plant: PlantModel):
    results = {}
    for unit in plant.units:
        p = unit.parameters
        if unit.type == "rapid_mix":
            results[unit.id] = rapid_mix(
                p["Q_m3_s"], p["volume_m3"], p.get("G_s", 60)
            )
        elif unit.type == "flocculation":
            results[unit.id] = flocculation(
                p["Q_m3_s"], p["volume_m3"], p.get("G_s", 30)
            )
        elif unit.type == "sedimentation":
            results[unit.id] = sedimentation(
                p["Q_m3_s"], p["area_m2"], p["depth_m"]
            )
        elif unit.type == "filtration":
            results[unit.id] = filtration(p["Q_m3_s"], p["area_m2"])
        elif unit.type == "disinfection":
            results[unit.id] = disinfection(
                p["Q_m3_s"], p["volume_m3"], p.get("chlorine_mg_l", 1.5)
            )
    return {"plant_id": plant.id, "plant_name": plant.name, "units": results}
