#!/usr/bin/env python3
"""
Demostración de HYDROCALC-PTAP v0.1

Este script muestra las capacidades principales del motor de cálculo:
1. Sistema de unidades
2. Constantes físicas
3. Validación
4. Diseño de floculación
5. Dosificación de coagulantes
"""

import sys
from pathlib import Path

# Agregar el directorio raíz al path
sys.path.insert(0, str(Path(__file__).parent))

print("=" * 70)
print("           HYDROCALC-PTAP v0.1 - DEMOSTRACIÓN")
print("        Plataforma de Cálculo para Ingeniería del Agua")
print("=" * 70)
print()


# =============================================================================
# 1. SISTEMA DE UNIDADES
# =============================================================================
print("\n" + "=" * 70)
print("1. SISTEMA DE UNIDADES")
print("=" * 70)

from core.units import convert, convert_to_si, format_value, list_available_units

print("\nConversiones comunes:")
print("-" * 50)

# Caudal
q_l_s = 500
q_m3_s = convert(q_l_s, "L_s", "m3_s")
print(f"  {format_value(q_l_s, 'L_s')} = {format_value(q_m3_s, 'm3_s')}")

# Tiempo
t_min = 25
t_s = convert(t_min, "min", "s")
print(f"  {format_value(t_min, 'min')} = {format_value(t_s, 's')}")

# Volumen
v_L = 1000
v_m3 = convert(v_L, "L", "m3")
print(f"  {format_value(v_L, 'L')} = {format_value(v_m3, 'm3')}")

# Concentración
c_mg_L = 25
c_kg_m3 = convert(c_mg_L, "mg_L", "kg_m3")
print(f"  {format_value(c_mg_L, 'mg_L')} = {format_value(c_kg_m3, 'kg_m3')}")

# Potencia
p_W = 2704
p_kW = convert(p_W, "W", "kW")
print(f"  {format_value(p_W, 'W')} = {format_value(p_kW, 'kW')}")

print(f"\nUnidades disponibles por tipo:")
units_by_type = list_available_units()
for unit_type, units in list(units_by_type.items())[:5]:
    print(f"  {unit_type}: {', '.join(units[:4])}...")


# =============================================================================
# 2. CONSTANTES FÍSICAS
# =============================================================================
print("\n" + "=" * 70)
print("2. CONSTANTES FÍSICAS Y PARÁMETROS")
print("=" * 70)

from core.constants import (
    get_water_properties,
    get_design_parameter,
    check_parameter_range,
    get_chemical,
    list_chemicals
)

print("\nPropiedades del agua a diferentes temperaturas:")
print("-" * 50)
for temp in [10, 20, 30]:
    props = get_water_properties(temp)
    print(f"  {temp}°C: ρ={props.density:.2f} kg/m³, μ={props.viscosity_dynamic:.4e} Pa·s")

print("\nParámetros de diseño para floculación:")
print("-" * 50)
params = ['G', 'T', 'GT']
for param in params:
    p = get_design_parameter('flocculation', param)
    if p:
        print(f"  {p.symbol}: {p.name}")
        print(f"      Rango: {p.min_value} - {p.max_value} {p.unit}")
        print(f"      Típico: {p.typical_value} {p.unit}")

print("\nQuímicos disponibles (coagulantes):")
print("-" * 50)
coagulants = list_chemicals('coagulación')
for chem_name in coagulants[:5]:
    chem = get_chemical(chem_name)
    print(f"  {chem.name} ({chem.formula})")


# =============================================================================
# 3. VALIDACIÓN
# =============================================================================
print("\n" + "=" * 70)
print("3. SISTEMA DE VALIDACIÓN")
print("=" * 70)

from core.validation import PTAPValidator, ValidationLevel

validator = PTAPValidator()

print("\nValidación de caudal (500 L/s):")
print("-" * 50)
result = validator.validate_flow(500, "L_s")
status = "✓ VÁLIDO" if result.is_valid else "✗ INVÁLIDO"
print(f"  Estado: {status}")
for msg in result.messages:
    icon = {'info': 'ℹ', 'warning': '⚠', 'error': '❌'}[msg.level.value]
    print(f"  {icon} {msg.message}")

print("\nValidación de gradiente de velocidad (G = 100 s⁻¹, fuera de rango):")
print("-" * 50)
result = validator.validate_velocity_gradient(100, "flocculation")
status = "✓ VÁLIDO" if result.is_valid else "✗ INVÁLIDO"
print(f"  Estado: {status}")
for msg in result.messages:
    icon = {'info': 'ℹ', 'warning': '⚠', 'error': '❌'}[msg.level.value]
    print(f"  {icon} {msg.message}")


# =============================================================================
# 4. DISEÑO DE FLOCULACIÓN
# =============================================================================
print("\n" + "=" * 70)
print("4. DISEÑO DE FLOCULACIÓN")
print("=" * 70)

from ptap.flocculation.design import FlocculationInput, design_flocculation

inputs = FlocculationInput(
    flow=500,              # L/s
    detention_time=25,     # min
    velocity_gradient=60,  # s⁻¹
    water_temperature=20,  # °C
    num_chambers=3         # cámaras en serie
)

print("\nDatos de entrada:")
print("-" * 50)
print(f"  Caudal: {inputs.flow} {inputs.flow_unit}")
print(f"  Tiempo de retención: {inputs.detention_time} {inputs.time_unit}")
print(f"  Gradiente G: {inputs.velocity_gradient} {inputs.gradient_unit}")
print(f"  Temperatura: {inputs.water_temperature} °C")
print(f"  Número de cámaras: {inputs.num_chambers}")

result = design_flocculation(inputs)

print("\nResultados:")
print("-" * 50)
print(f"  Volumen total: {result.volume:.2f} m³")
print(f"  Potencia requerida: {result.power:.2f} W ({result.power/1000:.3f} kW)")
print(f"  Número de Camp (GT): {result.gt_number:.0f}")
print(f"  Volumen por cámara: {result.volume_per_chamber:.2f} m³")

if result.dimensions:
    print("\nDimensiones estimadas:")
    print(f"  Profundidad: {result.dimensions['depth']:.2f} m")
    print(f"  Ancho: {result.dimensions['width']:.2f} m")
    print(f"  Largo por cámara: {result.dimensions['length']:.2f} m")
    print(f"  Largo total: {result.dimensions['length_total']:.2f} m")

print(f"\nValidación: {'✓ VÁLIDO' if result.validation_result.is_valid else '✗ INVÁLIDO'}")

if result.warnings:
    print("Advertencias:")
    for w in result.warnings:
        print(f"  ⚠ {w}")

if result.info:
    print("Información:")
    for info in result.info[:3]:
        print(f"  ℹ {info}")


# =============================================================================
# 5. DOSIFICACIÓN DE COAGULANTES
# =============================================================================
print("\n" + "=" * 70)
print("5. DOSIFICACIÓN DE COAGULANTES")
print("=" * 70)

from ptap.coagulation.dosage import CoagulantDosageInput, calculate_coagulant_dosage

inputs = CoagulantDosageInput(
    flow=500,              # L/s
    dose=25,               # mg/L
    chemical_name='alum',  # sulfato de aluminio
    solution_concentration=10,  # % p/p
    operating_hours=24
)

print("\nDatos de entrada:")
print("-" * 50)
print(f"  Caudal: {inputs.flow} {inputs.flow_unit}")
print(f"  Dosis: {inputs.dose} {inputs.dose_unit}")
print(f"  Químico: {inputs.chemical_name}")
print(f"  Concentración solución: {inputs.solution_concentration}%")

result = calculate_coagulant_dosage(inputs)

print("\nResultados:")
print("-" * 50)
print(f"  Químico: {result.chemical_info['name']}")
print(f"  Fórmula: {result.chemical_info['formula']}")
print(f"  Pureza: {result.purity_used}%")
print()
print(f"  Consumo diario: {result.daily_mass:.2f} kg/d")
print(f"  Consumo horario: {result.hourly_mass:.3f} kg/h")
print(f"  Caudal de solución: {result.solution_flow_rate:.2f} {result.solution_flow_unit}")

print("\nEstimaciones:")
monthly = result.daily_mass * 30
annual = result.daily_mass * 365
print(f"  Mensual: {monthly:.1f} kg/mes")
print(f"  Anual: {annual:.1f} kg/año")

print(f"\nValidación: {'✓ VÁLIDO' if result.validation_result.is_valid else '✗ INVÁLIDO'}")


# =============================================================================
# RESUMEN
# =============================================================================
print("\n" + "=" * 70)
print("RESUMEN")
print("=" * 70)
print("""
HYDROCALC-PTAP v0.1 ha demostrado exitosamente:

✅ Sistema de unidades con conversión automática
✅ Base de datos de propiedades físicas y químicas
✅ Validación física con warnings y errores
✅ Diseño de floculadores (volumen, potencia, GT, dimensiones)
✅ Cálculo de dosificación de coagulantes
✅ Generación de información técnica detallada

Próximas fases:
→ Interfaz web Streamlit
→ Gráficos y visualizaciones
→ Memorias de cálculo PDF/Excel
→ Análisis dinámico y SciML
""")

print("=" * 70)
print("                    FIN DE LA DEMOSTRACIÓN")
print("=" * 70)
