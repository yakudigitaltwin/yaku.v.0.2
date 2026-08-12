# Estructura del Código y Previsualización - Yaku-Digital Twin

## 📋 Descripción General

Yaku-Digital Twin es una plataforma para cálculo, diseño y simulación de Plantas de Tratamiento de Agua Potable (PTAP). El proyecto está organizado en múltiples componentes que trabajan juntos.

---

## 🏗️ Estructura del Proyecto

```
/workspace
├── backend/                 # API REST con FastAPI (Python)
│   ├── app/
│   │   ├── api/            # Endpoints de la API
│   │   │   └── routes.py   # Rutas: /classic/demo, /classic/design, /classic/simulate
│   │   ├── calculations/   # Lógica de cálculos de ingeniería
│   │   │   ├── design.py          # Cálculos de diseño de unidades
│   │   │   └── classic_ponder.py  # Cálculos de ponderación clásica
│   │   ├── domain/         # Modelos de dominio
│   │   │   ├── plant.py           # PlantaModel
│   │   │   ├── process_unit.py    # ProcessUnit
│   │   │   └── stream.py          # Stream (conexiones)
│   │   ├── services/       # Servicios de negocio
│   │   │   └── classic_service.py # Construcción, diseño y simulación
│   │   ├── main.py         # Punto de entrada FastAPI
│   │   └── schemas.py      # Esquemas Pydantic para request/response
│   ├── tests/              # Pruebas unitarias
│   └── requirements.txt    # Dependencias Python
│
├── frontend/               # Interfaz React + TypeScript + Vite
│   ├── src/
│   │   ├── components/     # Componentes React
│   │   │   ├── App.tsx             # Componente principal
│   │   │   ├── ProcessBuilder.tsx  # Editor gráfico de procesos
│   │   │   ├── ProcessNode.tsx     # Nodo de unidad de proceso
│   │   │   ├── PropertiesPanel.tsx # Panel de propiedades
│   │   │   └── ConnectionLine.tsx  # Líneas de conexión SVG
│   │   ├── types/
│   │   │   └── process.ts          # Tipos TypeScript
│   │   ├── main.tsx        # Punto de entrada React
│   │   └── styles.css      # Estilos globales
│   ├── index.html
│   ├── package.json
│   └── vite.config.ts
│
├── hydrocalc_ptap/         # Motor de cálculo científico (Python)
│   ├── core/               # Núcleo
│   │   ├── units.py        # Sistema de conversión de unidades
│   │   ├── constants.py    # Constantes físicas y químicas
│   │   └── validation.py   # Validador PTAP
│   ├── ptap/               # Procesos unitarios PTAP
│   │   ├── coagulation/
│   │   │   └── dosage.py   # Dosificación de coagulantes
│   │   └── flocculation/
│   │       └── design.py   # Diseño de floculadores
│   ├── reports/            # Generación de reportes
│   ├── database/           # Capa de datos
│   ├── tests/              # Pruebas
│   └── demo.py             # Demostración interactiva
│
├── scientific/julia/       # Motor dinámico (Julia)
│   ├── src/
│   │   └── YakuDigitalTwin.jl  # Módulo principal
│   ├── scripts/
│   │   └── run_dynamic.jl      # Script de simulación dinámica
│   └── Project.toml            # Dependencias Julia
│
└── docs/                   # Documentación
    ├── ROADMAP.md          # Hoja de ruta del proyecto
    ├── CLASSIC_PONDER.md   # Documentación de ponderación clásica
    ├── MODEL_SPEC.md       # Especificaciones de modelos
    └── PROCESS_BUILDER.md  # Guía del constructor de procesos
```

---

## 🔧 Componentes Principales

### 1. Backend (FastAPI - Python)

**Ubicación:** `/workspace/backend`

**Funcionalidad:**
- API REST para cálculos de PTAP
- Modelos de dominio: `PlantModel`, `ProcessUnit`, `Stream`
- Cálculos de diseño para: coagulación, floculación, sedimentación, filtración, desinfección
- Simulación dinámica simplificada

**Endpoints principales:**
- `GET /api/v1/classic/demo` - Obtiene planta demo preconfigurada
- `POST /api/v1/classic/design` - Diseña una planta completa
- `POST /api/v1/classic/simulate` - Ejecuta simulación dinámica
- `POST /api/v1/classic/calculate-unit` - Calcula unidad específica
- `POST /api/v1/classic/ponder` - Realiza cálculo de ponderación clásica

**Archivos clave:**
- `app/main.py` - Configuración de FastAPI y CORS
- `app/api/routes.py` - Definición de endpoints
- `app/services/classic_service.py` - Lógica de negocio principal
- `app/calculations/design.py` - Fórmulas de diseño hidráulico
- `app/calculations/classic_ponder.py` - Sistema de validación y scoring

---

### 2. Frontend (React + TypeScript + Vite)

**Ubicación:** `/workspace/frontend`

**Funcionalidad:**
- Interfaz gráfica tipo "drag-and-drop" para construir flujos de proceso
- Panel de propiedades para editar parámetros de cada unidad
- Visualización de resultados de simulación
- Conexiones visuales entre unidades (SVG)

**Componentes:**
- `App.tsx` - Contenedor principal y gestión de estado
- `ProcessBuilder.tsx` - Canvas interactivo con paleta de unidades
- `ProcessNode.tsx` - Representación visual de cada unidad
- `PropertiesPanel.tsx` - Formulario de edición de parámetros
- `ConnectionLine.tsx` - Renderizado de conexiones entre nodos

**Unidades disponibles:**
| Tipo | Icono | Nombre | Parámetros principales |
|------|-------|--------|----------------------|
| source | 💧 | Fuente | Q_m3_s, turbidity_ntu, pH |
| rapid_mix | ⚗ | Coagulación | Q_m3_s, volume_m3, G_s, coagulant_mg_l |
| flocculation | 🌊 | Floculación | Q_m3_s, volume_m3, G_s |
| sedimentation | 🏞 | Sedimentación | Q_m3_s, area_m2, depth_m |
| filtration | 🔬 | Filtración | Q_m3_s, area_m2, headloss_m |
| disinfection | 🧪 | Desinfección | Q_m3_s, volume_m3, chlorine_mg_l |
| tank | 💧 | Tanque | Q_m3_s, volume_m3 |

---

### 3. HydroCalc PTAP (Motor Científico)

**Ubicación:** `/workspace/hydrocalc_ptap`

**Funcionalidad:**
- Sistema de unidades con conversión automática
- Base de datos de propiedades físicas del agua
- Validación física con warnings y errores
- Diseño detallado de floculadores
- Cálculo de dosificación de coagulantes

**Módulos principales:**
- `core/units.py` - Conversiones: L/s ↔ m³/s, mg/L ↔ kg/m³, etc.
- `core/constants.py` - Propiedades del agua, parámetros de diseño, químicos
- `core/validation.py` - Validador PTAP con niveles de severidad
- `ptap/flocculation/design.py` - Cálculo de volumen, potencia, GT, dimensiones
- `ptap/coagulation/dosage.py` - Consumo diario, caudal de solución

**Ejecutar demo:**
```bash
cd /workspace/hydrocalc_ptap
python demo.py
```

---

### 4. Scientific Julia (Simulación Dinámica)

**Ubicación:** `/workspace/scientific/julia`

**Funcionalidad:**
- Motor de ecuaciones diferenciales ordinarias (ODE)
- Simulación de decaimiento de cloro en tiempo real
- Integración futura con Python vía PyJulia

**Archivo principal:**
- `src/YakuDigitalTwin.jl` - Módulo con función `simulate_chlorine_decay`
- `scripts/run_dynamic.jl` - Script de ejemplo

**Requisitos:** Julia 1.10+

---

## 🚀 Cómo Previsualizar/Ejecutar

### Opción 1: Docker Compose (Recomendado)

```bash
cd /workspace
docker compose up --build
```

Esto levantará:
- Backend en http://localhost:8000
- Frontend en http://localhost:5173
- Swagger UI en http://localhost:8000/docs

---

### Opción 2: Ejecución Manual

#### Backend (Terminal 1)
```bash
cd /workspace/backend
python -m venv .venv
source .venv/bin/activate  # En Windows: .venv\Scripts\activate
pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

**Verificar backend:**
```bash
curl http://localhost:8000/health
# Respuesta: {"status":"ok","service":"yaku-backend","version":"0.1.0"}
```

**Probar endpoint demo:**
```bash
curl http://localhost:8000/api/v1/classic/demo
```

#### Frontend (Terminal 2)
```bash
cd /workspace/frontend
npm install
npm run dev -- --host 0.0.0.0
```

Acceder a: http://localhost:5173

---

### Opción 3: Solo HydroCalc PTAP

```bash
cd /workspace/hydrocalc_ptap
python demo.py
```

Salida esperada:
```
======================================================================
           HYDROCALC-PTAP v0.1 - DEMOSTRACIÓN
        Plataforma de Cálculo para Ingeniería del Agua
======================================================================

1. SISTEMA DE UNIDADES
--------------------------------------------------
  500.00 L_s = 0.50 m3_s
  25.00 min = 1500.00 s
  ...

2. CONSTANTES FÍSICAS Y PARÁMETROS
...
```

---

### Opción 4: Solo Julia (Simulación Dinámica)

```bash
cd /workspace/scientific/julia
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. scripts/run_dynamic.jl
```

Salida esperada:
```
Yaku Julia dynamic engine
C inicial = 1.5 mg/L
C final   = 0.XX mg/L
```

---

## 🧪 Pruebas de Funcionamiento

### Test Backend
```bash
cd /workspace/backend
python -m pytest tests/ -v
```

### Test HydroCalc
```bash
cd /workspace/hydrocalc_ptap
python -m pytest tests/ -v
```

### Test Unit Calculation (Backend)
```bash
cd /workspace/backend
python test_unit_calculation.py
```

### Test Service Function (Backend)
```bash
cd /workspace/backend
python test_service_function.py
```

---

## 📊 Flujo de Datos Típico

```
┌─────────────┐     POST /classic/design     ┌──────────────┐
│   Frontend  │ ───────────────────────────► │   Backend    │
│  (React)    │                              │  (FastAPI)   │
│             │ ◄─────────────────────────── │              │
│             │     JSON con resultados      │              │
└─────────────┘                              └──────┬───────┘
                                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │  Calculations  │
                                          │  (design.py)   │
                                          └────────────────┘
                                                   │
                                                   ▼
                                          ┌────────────────┐
                                          │  Domain Models │
                                          │  (PlantModel)  │
                                          └────────────────┘
```

---

## 🔍 Endpoints de la API - Ejemplos

### 1. Obtener planta demo
```bash
curl http://localhost:8000/api/v1/classic/demo | jq
```

### 2. Diseñar planta personalizada
```bash
curl -X POST http://localhost:8000/api/v1/classic/design \
  -H "Content-Type: application/json" \
  -d '{
    "id": "mi-ptap",
    "name": "Mi PTAP",
    "units": [
      {
        "id": "fuente",
        "type": "source",
        "name": "Agua cruda",
        "parameters": {"Q_m3_s": 0.5, "turbidity_ntu": 20}
      },
      {
        "id": "mezcla",
        "type": "rapid_mix",
        "name": "Mezcla rápida",
        "parameters": {"Q_m3_s": 0.5, "volume_m3": 30, "G_s": 60}
      }
    ],
    "streams": []
  }' | jq
```

### 3. Calcular unidad específica
```bash
curl -X POST http://localhost:8000/api/v1/classic/calculate-unit \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": "sed-1",
    "unit_type": "sedimentation",
    "parameters": {"Q_m3_s": 0.5, "area_m2": 1500, "depth_m": 4},
    "calculation_type": "design"
  }' | jq
```

### 4. Ponderación clásica
```bash
curl -X POST http://localhost:8000/api/v1/classic/ponder \
  -H "Content-Type: application/json" \
  -d '{
    "unit_id": "floc-1",
    "unit_type": "flocculation",
    "parameters": {"Q_m3_s": 0.5, "volume_m3": 750, "G_s": 30},
    "calculation_type": "design"
  }' | jq
```

---

## 🛠️ Tecnologías Utilizadas

| Componente | Tecnología | Versión |
|------------|-----------|---------|
| Backend | Python + FastAPI | 3.10+ |
| Frontend | React + TypeScript | 18.x |
| Build Tool | Vite | 5.x |
| Drag & Drop | react-dnd | 16.x |
| Validación | Pydantic | 2.x |
| Cálculo Numérico | NumPy | 1.x |
| ODE Solver | Julia + DifferentialEquations.jl | 1.10+ |
| Contenerización | Docker Compose | 2.x |

---

## 📈 Roadmap (Próximas Versiones)

- **v0.2**: Editor gráfico con React Flow/XYFlow
- **v0.3**: PostgreSQL/PostGIS + persistencia de proyectos
- **v0.4**: Simulación dinámica por bloques + integración Python-Julia
- **v0.5**: Model Lab (DMD, POD, ROM, PINN, KAN)
- **v0.6**: Control PID
- **v0.7**: Digital Twin completo + MQTT + SCADA
- **v1.0**: Autenticación + auditoría + cloud

---

## ⚠️ Advertencias Importantes

> Los modelos de v0.1 son **preliminares y educativos**. Deben validarse con:
> - Ensayayos de laboratorio (pruebas de jarra)
> - Datos de operación real
> - Normativa aplicable local
> - Revisión de profesional colegiado

**NO USAR para diseño real sin validación adecuada.**

---

## 📞 Soporte y Contribución

Para más información consultar:
- `/workspace/README.md` - Guía rápida
- `/workspace/docs/` - Documentación detallada
- `/workspace/hydrocalc_ptap/README.md` - Documentación de HydroCalc

---

*Documento generado para Yaku-Digital Twin v0.1 - Classic PTAP Design & Simulation Platform*
