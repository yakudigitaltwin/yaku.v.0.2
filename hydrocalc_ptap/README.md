# HYDROCALC-PTAP v0.1

**Plataforma de cálculo para ingeniería del agua - PTAP, coagulación y floculación**

HYDROCALC-PTAP es un motor de cálculo especializado en tratamiento de agua potable (PTAP), inspirado en la filosofía de PlutoCalc pero diseñado específicamente para ingeniería sanitaria con capacidades avanzadas de validación, trazabilidad y generación de memorias de cálculo.

## 🚀 Características Principales

### Núcleo de Cálculo
- ✅ **Sistema de unidades completo**: Conversión automática entre unidades comunes en ingeniería del agua
- ✅ **Validación física**: Verificación de rangos, consistencia dimensional y detección de errores
- ✅ **Parámetros normativos**: Rangos recomendados según AWWA, ASCE, WHO, EPA
- ✅ **Base de datos de químicos**: Propiedades de coagulantes, desinfectantes y ayudantes

### Módulos Disponibles (v0.1)

#### 1. Floculación (`ptap.flocculation.design`)
- Volumen del floculador
- Potencia requerida (ecuación de Camp-Stein)
- Número de Camp (GT)
- Dimensiones estimadas del tanque
- Floculación escalonada con gradiente decreciente

#### 2. Dosificación de Coagulantes (`ptap.coagulation.dosage`)
- Cálculo de consumo diario/horario
- Caudal de solución química
- Optimización de dosis
- Requerimientos de almacenamiento

## 📦 Instalación

```bash
cd hydrocalc_ptap
pip install -e ".[dev]"
```

## 💻 Uso Básico

### Ejemplo: Diseño de Floculador

```python
from ptap.flocculation.design import FlocculationInput, design_flocculation

# Definir parámetros de diseño
inputs = FlocculationInput(
    flow=500,              # L/s
    detention_time=25,     # min
    velocity_gradient=60,  # s⁻¹
    water_temperature=20,  # °C
    num_chambers=3         # cámaras en serie
)

# Ejecutar cálculo
result = design_flocculation(inputs)

print(f"Volumen: {result.volume:.2f} m³")
print(f"Potencia: {result.power/1000:.3f} kW")
print(f"GT: {result.gt_number:.0f}")
```

### Ejemplo: Dosificación de Coagulante

```python
from ptap.coagulation.dosage import CoagulantDosageInput, calculate_coagulant_dosage

inputs = CoagulantDosageInput(
    flow=500,              # L/s
    dose=25,               # mg/L
    chemical_name='alum',  # sulfato de aluminio
    solution_concentration=10  # % p/p
)

result = calculate_coagulant_dosage(inputs)

print(f"Consumo diario: {result.daily_mass:.2f} kg/d")
print(f"Caudal solución: {result.solution_flow_rate:.2f} mL/min")
```

## 🧪 Ejecutar Tests

```bash
pytest tests/ -v
```

## 🏗️ Arquitectura del Proyecto

```
hydrocalc_ptap/
│
├── core/                    # Núcleo del sistema
│   ├── units.py            # Sistema de unidades
│   ├── constants.py        # Constantes y parámetros
│   └── validation.py       # Validación física
│
├── ptap/                    # Procesos PTAP
│   ├── coagulation/
│   │   └── dosage.py       # Dosificación de coagulantes
│   └── flocculation/
│       └── design.py       # Diseño de floculadores
│
├── app/                     # Interfaz Streamlit (próximamente)
├── reports/                 # Generación de PDF/Excel (próximamente)
├── database/                # Base de datos de químicos
└── tests/                   # Tests unitarios
```

## 📊 Roadmap

### Fase 1 — Motor ✅ (COMPLETADO)
- [x] Sistema de unidades
- [x] Constantes físicas
- [x] Validación
- [x] Tests automáticos

### Fase 2 — Coagulación ✅ (COMPLETADO)
- [x] Dosis de coagulante
- [x] Soluciones químicas
- [x] Consumo diario/mensual

### Fase 3 — Floculación ✅ (COMPLETADO)
- [x] Volumen y potencia
- [x] Número de Camp
- [x] Dimensiones estimadas

### Fase 4 — Interfaz Web (PRÓXIMAMENTE)
- [ ] Aplicación Streamlit tipo PlutoCalc
- [ ] Navegación por categorías
- [ ] Inputs con selección de unidades

### Fase 5 — Gráficos (PRÓXIMAMENTE)
- [ ] Curvas de sensibilidad
- [ ] Perfiles de gradiente
- [ ] Comparación de alternativas

### Fase 6 — Memorias de Cálculo (PRÓXIMAMENTE)
- [ ] Exportación a PDF
- [ ] Exportación a Excel
- [ ] Formato profesional con ecuaciones

### Fase 7 — Análisis Dinámico (FUTURO)
- [ ] Modelo dinámico de floculación
- [ ] Puntos de equilibrio
- [ ] Estabilidad (Jacobiano, autovalores)
- [ ] Retratos de fase

### Fase 8 — SciML (FUTURO)
- [ ] SINDy (identificación de ecuaciones)
- [ ] Neural ODE / UDE
- [ ] PINN / PI-KAN
- [ ] Koopman

### Fase 9 — Gemelo Digital (FUTURO)
- [ ] Conexión SCADA/IoT
- [ ] Predicción en tiempo real
- [ ] Optimización y control

## 📖 Referencias Técnicas

- **AWWA M37** - Operational Control of Coagulation and Filtration Processes
- **ASCE** - Water Treatment Plant Design
- **Camp, T. R., & Stein, P. C. (1943)** - Velocity gradients and internal work in fluid motion
- **WHO** - Guidelines for Drinking-water Quality

## 🔧 Desarrollo

```bash
# Instalar en modo desarrollo
pip install -e ".[dev]"

# Ejecutar tests
pytest tests/ -v

# Formatear código
black .

# Verificar tipos
mypy .
```

## 📄 Licencia

MIT License

## 👥 Autores

HydroCalc Team - Ingeniería del Agua + SciML

---

**HYDROCALC-PTAP** es software de código abierto en desarrollo activo. Contribuciones son bienvenidas.
