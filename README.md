# Yaku-Digital Twin — Yaku Classic v0.1

MVP experimental para cálculo, diseño y simulación de Plantas de Tratamiento de Agua Potable (PTAP).

## Incluye

- PlantModel, ProcessUnit y Stream.
- Coagulación/mezcla rápida.
- Floculación.
- Sedimentación.
- Filtración.
- Desinfección.
- Cálculo estacionario en Python.
- Primer motor dinámico ODE en Julia.
- API REST FastAPI.
- Interfaz React + TypeScript + Vite.
- Docker Compose.

> Los modelos de v0.1 son preliminares y educativos. Deben validarse con ensayos, datos de operación, normativa aplicable y revisión profesional antes de usarse para diseño real.

## Backend

```bash
cd backend
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

API: http://localhost:8000
Swagger: http://localhost:8000/docs

## Frontend

```bash
cd frontend
npm install
npm run dev
```

Frontend: http://localhost:5173

## Julia

Requiere Julia 1.10+.

```bash
cd scientific/julia
julia --project=. -e 'using Pkg; Pkg.instantiate()'
julia --project=. scripts/run_dynamic.jl
```

## Docker

```bash
docker compose up --build
```

## Roadmap

v0.2: editor gráfico React Flow/XYFlow.
v0.3: PostgreSQL/PostGIS y persistencia.
v0.4: integración Python-Julia y simulación dinámica por bloques.
v0.5: Model Lab: DMD, POD, ROM, PINN y KAN.
v0.6: PID.
v0.7: Digital Twin, MQTT y SCADA.
