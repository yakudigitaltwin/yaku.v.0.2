# Requirements Document

## Introduction

This spec defines the requirements for implementing and launching the Yaku Digital Twin MVP. The Yaku Digital Twin is a Water Treatment Plant (PTAP) simulation platform that provides modeling, design, and simulation capabilities for potable water treatment processes. The current v0.1 MVP exists with basic functionality but needs comprehensive implementation and launch tasks defined.

## Glossary

- **Yaku**: The Water Treatment Plant simulation platform
- **PTAP**: Plantas de Tratamiento de Agua Potable (Potable Water Treatment Plants)
- **MVP**: Minimum Viable Product - initial release with core functionality
- **Backend**: Python/FastAPI server providing plant modeling, process calculations, and API endpoints
- **Frontend**: React + TypeScript + Vite client for visualization and user interaction
- **Scientific Engine**: Julia-based ODE solver for dynamic simulation
- **Process Unit**: Individual treatment stage (coagulation, flocculation, sedimentation, filtration, disinfection)
- **Steady-State Calculation**: Design parameters for treatment units at constant flow conditions
- **Dynamic Simulation**: Time-based ODE simulation of treatment processes

## Requirements

### Requirement 1: Core Plant Modeling

**User Story:** As an engineer, I want to model a complete water treatment plant, so that I can simulate its behavior and performance.

#### Acceptance Criteria

1. THE Yaku Backend SHALL represent a Plant as a collection of interconnected Process Units with defined flows
2. EACH Process Unit SHALL have a unique identifier, type, name, and parameter dictionary
3. EACH Process Unit SHALL have a state dictionary for runtime values
4. THE Yaku Backend SHALL support at minimum: source, coagulation, flocculation, sedimentation, filtration, disinfection, and sink units
5. WHILE a plant model exists, THE Yaku Backend SHALL maintain stream connections between units with flow rates and water quality data

### Requirement 2: Process Unit Calculations

**User Story:** As an engineer, I want to calculate design parameters for treatment units, so that I can verify sizing and performance.

#### Acceptance Criteria

1. WHEN a rapid mix calculation is requested, THE Design Calculator SHALL compute detention time (s, min) and power requirement (W)
2. WHEN a flocculation calculation is requested, THE Design Calculator SHALL compute detention time (s, min) and Gt value
3. WHEN a sedimentation calculation is requested, THE Design Calculator SHALL compute surface overflow rate (m/s, m/h), volume (m³), and detention time (h)
4. WHEN a filtration calculation is requested, THE Design Calculator SHALL compute filtration rate (m/h)
5. WHEN a disinfection calculation is requested, THE Design Calculator SHALL compute contact time (min) and CT value (mg·min/L)

### Requirement 3: API Endpoints

**User Story:** As a frontend developer, I want REST API endpoints for plant operations, so that I can build interactive visualizations.

#### Acceptance Criteria

1. THE API SHALL provide a GET /api/v1/classic/demo endpoint that returns a pre-configured demo plant
2. THE API SHALL provide a POST /api/v1/classic/design endpoint that accepts a PlantRequest and returns calculated design parameters
3. THE API SHALL provide a POST /api/v1/classic/simulate endpoint that accepts a SimulationRequest and returns time-series state data
4. THE API SHALL provide a POST /api/v1/classic/calculate-unit endpoint that accepts calculation parameters and returns unit-specific results
5. THE API SHALL include /health endpoint returning service status and version

### Requirement 4: Frontend Visualization

**User Story:** As an operator, I want to visualize the treatment plant layout and results, so that I can understand process behavior.

#### Acceptance Criteria

1. WHEN the frontend loads, THE UI SHALL fetch and display the demo plant from the backend API
2. WHILE displaying plant units, THE UI SHALL show process units in flow order with unit types and names
3. THE UI SHALL provide a "Calcular diseño" button that triggers design calculations and displays results
4. WHERE units have calculation results, THE UI SHALL display parameter names and values in formatted output
5. THE UI SHALL display error messages immediately when any API call fails

### Requirement 5: Dynamic Simulation Engine

**User Story:** As a scientist, I want to run dynamic ODE simulations for time-varying processes, so that I can model real-world treatment behavior.

#### Acceptance Criteria

1. WHEN dynamic simulation is invoked, THE Julia Engine SHALL solve ODEs for chlorine decay using the Tsit5 integrator with no fallback options
2. WHILE simulation runs, THE Julia Engine SHALL save state at specified time intervals
3. THE Julia Engine SHALL return time series data for chlorine concentration (mg/L) over the simulation period
4. FOR ALL valid inputs, THE Julia Engine SHALL return chlorine concentration time series data even when concentration is zero at all time points

### Requirement 6: Deployment and Orchestration

**User Story:** As a DevOps engineer, I want containerized deployment, so that I can easily run the complete system.

#### Acceptance Criteria

1. WHEN docker compose up is executed, THE Docker Compose SHALL start the backend service on port 8000 and the frontend service on port 5173
2. WHILE services are running, THE Backend AND Frontend SHALL communicate via CORS configuration
3. THE Docker Compose configuration SHALL mount local directories for development hot-reload

### Requirement 7: Data Integrity

**User Story:** As a developer, I want consistent data handling, so that my calculations are reliable and reproducible.

#### Acceptance Criteria

1. FOR ALL input values, IF any parameter is zero or negative, THEN THE Calculator SHALL return an error with descriptive message
2. FOR ALL design calculations, THE Output SHALL include all required parameters with non-null values
3. WHEN simulation completes, THE Result SHALL include plant identification, duration, time step, and complete state array
4. WHERE a process unit is not found, THE Backend SHALL return HTTP 404 with clear error identification

### Requirement 8: Documentation and Validation

**User Story:** As a engineer, I want clear documentation and validation notes, so that I understand model limitations.

#### Acceptance Criteria

1. THE Demo Plant Response SHALL include metadata indicating version "0.1" and purpose "demo"
2. THE Simulation Response SHALL include a model_note field stating results are preliminary and require validation
3. FOR ALL calculation results, THE API Response SHALL include timestamp metadata
4. WHERE user input validation fails, THE Response SHALL return HTTP 400 with detailed error description
