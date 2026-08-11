# Implementation Plan: Yaku Digital Twin MVP

## Overview

This implementation plan covers the complete Yaku Digital Twin MVP feature set across 8 core requirements:
- Core plant modeling with interconnected process units
- Design calculations for treatment units (rapid mix, flocculation, sedimentation, filtration, disinfection)
- REST API endpoints for plant operations
- Frontend visualization components
- Dynamic ODE simulation engine
- Docker Compose orchestration
- Data integrity validation
- Documentation

Tasks are organized to build functionality incrementally, with property-based tests validating correctness properties and unit tests covering edge cases.

## Tasks

- [ ] 1. Set up project structure and domain models
  - [ ] 1.1 Create PlantModel domain class with units and streams
    - Implement PlantModel with id, name, units, streams, parameters, and metadata fields
    - Add get_unit, upstream, and downstream methods for navigation
    - _Requirements: 1.1, 1.2, 1.3, 1.5_
  
  - [ ] 1.2 Create ProcessUnit domain class
    - Implement ProcessUnit with id, type, name, parameters, and states fields
    - Add parameter method for safe parameter access with defaults
    - _Requirements: 1.2, 1.3_
  
  - [ ] 1.3 Create Stream domain class
    - Implement Stream with id, source, target, flow_m3_s, and quality fields
    - _Requirements: 1.5_
  
  - [ ]* 1.4 Write property test for plant structure integrity
    - **Property 1: Plant Structure Integrity**
    - **Validates: Requirements 1.1, 1.2, 1.3, 1.5**
    - For any plant model, verify all units have required fields and streams reference valid units

- [ ] 2. Implement design calculations module
  - [ ] 2.1 Implement rapid_mix calculation function
    - Calculate detention time (s, min) and power requirement (W)
    - Validate Q and volume are positive, return error otherwise
    - _Requirements: 2.1, 7.1_
  
  - [ ] 2.2 Implement flocculation calculation function
    - Calculate detention time (s, min) and Gt value
    - Validate Q and volume are positive, return error otherwise
    - _Requirements: 2.2, 7.1_
  
  - [ ] 2.3 Implement sedimentation calculation function
    - Calculate surface overflow rate (m/s, m/h), volume (m³), and detention time (h)
    - Validate Q, area, and depth are positive, return error otherwise
    - _Requirements: 2.3, 7.1_
  
  - [ ] 2.4 Implement filtration calculation function
    - Calculate filtration rate (m/h)
    - Validate Q and area are positive, return error otherwise
    - _Requirements: 2.4, 7.1_
  
  - [ ] 2.5 Implement disinfection calculation function
    - Calculate contact time (min) and CT value (mg·min/L)
    - Validate Q and volume are positive, return error otherwise
    - _Requirements: 2.5, 7.1_
  
  - [ ]* 2.6 Write property test for unit calculation determinism
    - **Property 2: Unit Calculation Determinism**
    - **Validates: Requirements 2.1, 2.2, 2.3, 2.4, 2.5**
    - Verify deterministic results for valid inputs with all required fields present

- [ ] 3. Implement service layer for plant operations
  - [ ] 3.1 Implement build_demo_plant function
    - Create demo plant with 7 units (source, rapid_mix, flocculation, sedimentation, filtration, disinfection, sink)
    - Configure streams between units with flow rates
    - Include metadata with version "0.1" and purpose "demo"
    - _Requirements: 1.4, 8.1_
  
  - [ ] 3.2 Implement design_plant service function
    - Process all units in plant and call appropriate calculation functions
    - Return results as dictionary mapping unit_id to calculation results
    - _Requirements: 1.1, 2.x_
  
  - [ ] 3.3 Implement simulate_plant service function
    - Validate dt_s ≤ duration_s, raise ValueError if not
    - Compute time-series using simplified dynamic model
    - Include model_note field with validation notice
    - _Requirements: 5.1, 5.2, 5.3, 5.4, 7.3, 8.2_
  
  - [ ] 3.4 Implement calculate_unit service function
    - Route to appropriate calculation function based on unit_type
    - Support both "design" and "performance" calculation types
    - Return results with metadata timestamp
    - _Requirements: 7.2, 8.3_
  
  - [ ]* 3.5 Write unit tests for service layer
    - Test demo plant construction with correct unit count and streams
    - Test design_plant with various plant configurations
    - Test simulate_plant error handling for invalid parameters
    - _Requirements: 5.1, 6.1_

- [ ] 4. Implement API routes and schemas
  - [ ] 4.1 Create request/response Pydantic schemas
    - Define UnitRequest, StreamRequest, PlantRequest
    - Define ProcessUnitCalculationRequest and ProcessUnitCalculationResponse
    - Define SimulationRequest with validation (duration_s > 0, dt_s > 0)
    - Add to_domain methods for schema-to-model conversion
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 7.1_
  
  - [ ] 4.2 Implement /api/v1/classic/demo endpoint
    - Return demo plant using build_demo_plant()
    - Include metadata with version and purpose
    - _Requirements: 3.1, 8.1_
  
  - [ ] 4.3 Implement /api/v1/classic/design endpoint
    - Accept PlantRequest, call design_plant service
    - Return plant_id, plant_name, and units calculation results
    - _Requirements: 3.2, 7.2, 8.3_
  
  - [ ] 4.4 Implement /api/v1/classic/simulate endpoint
    - Accept SimulationRequest, validate parameters
    - Call simulate_plant service, handle ValueError with HTTP 400
    - Include model_note in response
    - _Requirements: 3.3, 5.1, 7.1, 7.3, 8.2, 8.4_
  
  - [ ] 4.5 Implement /api/v1/classic/calculate-unit endpoint
    - Accept ProcessUnitCalculationRequest
    - Call calculate_unit service with error handling
    - Return ProcessUnitCalculationResponse with metadata
    - _Requirements: 3.4, 7.1, 7.2, 8.3, 8.4_
  
  - [ ]* 4.6 Write integration tests for API endpoints
    - Test all endpoints with valid and invalid requests
    - Verify HTTP status codes (200, 400, 404)
    - Test CORS configuration
    - _Requirements: 3.x, 6.2, 8.4_

- [ ] 5. Extend frontend with plant visualization components
  - [ ] 5.1 Implement plant node rendering component
    - Create ProcessNode component for displaying units in flow order
    - Show unit type, name, and calculation results
    - Add arrow indicators between units
    - _Requirements: 4.1, 4.2, 4.3, 4.4_
  
  - [ ] 5.2 Implement result display component
    - Create ResultsGrid component for calculation results
    - Display parameter names and formatted values
    - Show error messages for API failures
    - _Requirements: 4.4, 4.5_
  
  - [ ]* 5.3 Write component tests for visualization
    - Test plant visualization renders units in correct order
    - Test result display shows calculation results correctly
    - _Requirements: 4.x_
  
  - [ ]* 5.4 Update App.tsx for improved state management
    - Add loading states for API calls
    - Implement proper error handling and display
    - _Requirements: 4.5_

- [ ] 6. Configure Docker Compose for deployment
  - [ ] 6.1 Update docker-compose.yml for backend service
    - Ensure backend builds from ./backend directory
    - Configure port 8000 mapping
    - Set environment variables for CORS configuration
    - Mount local directory for hot-reload
    - _Requirements: 6.1, 6.3_
  
  - [ ] 6.2 Update docker-compose.yml for frontend service
    - Use node:22-alpine image
    - Configure port 5173 mapping
    - Set up volume mounts for development
    - Ensure depends_on backend is configured
    - _Requirements: 6.1, 6.3_
  
  - [ ] 6.3 Create Dockerfile for backend
    - Use Python 3.11 slim image
    - Copy requirements.txt and install dependencies
    - Copy app directory
    - Set entrypoint to uvicorn
    - _Requirements: 6.1_
  
  - [ ]* 6.4 Write smoke test for Docker Compose
    - Test docker compose up starts both services
    - Verify backend responds on port 8000
    - Verify frontend responds on port 5173
    - Verify CORS allows frontend requests
    - _Requirements: 6.1, 6.2_

- [ ] 7. Implement data integrity and validation
  - [ ] 7.1 Add input validation to all calculation functions
    - Verify all parameters are positive (not zero or negative)
    - Return descriptive error messages for invalid inputs
    - _Requirements: 7.1, 8.4_
  
  - [ ] 7.2 Ensure all design calculation responses include complete parameters
    - Verify all required fields are present in results
    - Return non-null values for all parameters
    - _Requirements: 7.2, 8.3_
  
  - [ ] 7.3 Verify simulation responses include required metadata
    - Include plant_id, duration_s, dt_s, states array
    - Include model_note field with validation notice
    - _Requirements: 7.3, 8.2_
  
  - [ ] 7.4 Implement proper error handling for not-found units
    - Return HTTP 404 with clear error identification
    - _Requirements: 7.4_
  
  - [ ]* 7.5 Write property test for input validation
    - **Property 3: Input Validation**
    - **Validates: Requirements 7.1**
    - Verify zero and negative parameters are rejected with descriptive errors

- [ ] 8. Implement dynamic simulation engine integration
  - [ ] 8.1 Verify Julia ODE solver implementation
    - Confirm Tsit5 integrator is used (no fallback)
    - Test chlorine decay simulation with known inputs
    - Verify time-series output with correct time steps
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ] 8.2 Create Python wrapper for Julia simulation
    - Call Julia script with appropriate parameters
    - Parse JSON-compatible results
    - Handle errors and return appropriate HTTP responses
    - _Requirements: 5.1, 5.2, 5.3, 5.4_
  
  - [ ]* 8.3 Write property test for simulation time series
    - **Property 5: Simulation Time Series Structure**
    - **Validates: Requirements 5.2, 5.3, 5.4**
    - Verify time series has correct time steps and all required fields

- [ ] 9. Write property-based tests for correctness properties
  - [ ] 9.1 Write property test for stream connection validity
    - **Property 4: Stream Connection Validity**
    - **Validates: Requirement 1.5**
    - Verify all stream source/target IDs reference existing units
  
  - [ ] 9.2 Write property test for calculation results completeness
    - **Property 6: Calculation Results Completeness**
    - **Validates: Requirements 7.2, 8.3**
    - Verify all required output parameters present and non-null with metadata timestamp
  
  - [ ] 9.3 Write property test for simulation metadata inclusion
    - **Property 7: Simulation Metadata Inclusion**
    - **Validates: Requirements 7.3, 8.2**
    - Verify simulation responses include all required metadata fields
  
  - [ ] 9.4 Write property test for error response consistency
    - **Property 8: Error Response Consistency**
    - **Validates: Requirements 7.4, 8.4**
    - Verify invalid requests return appropriate HTTP status codes with descriptive messages
  
  - [ ] 9.5 Write property test for demo plant metadata
    - **Property 9: Demo Plant Metadata**
    - **Validates: Requirement 8.1**
    - Verify demo plant response includes version "0.1" and purpose "demo" in metadata

- [ ] 10. Update documentation and validation notes
  - [ ] 10.1 Update API documentation
    - Add OpenAPI/Swagger documentation for all endpoints
    - Document request/response schemas
    - Include example requests and responses
    - _Requirements: 3.x_
  
  - [ ] 10.2 Add model validation notes
    - Document model limitations in responses
    - Add notes about preliminary results requiring calibration
    - Document calculation simplifications
    - _Requirements: 8.2, 8.3_
  
  - [ ] 10.3 Update technical documentation
    - Document plant model structure and domain classes
    - Document calculation formulas and assumptions
    - Document testing strategy and property definitions
    - _Requirements: 1.x, 2.x, 5.x_

- [ ] 11. Checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 12. Integration and final validation
  - [ ] 12.1 Run integration test suite
    - Test complete plant workflow (create → calculate → simulate)
    - Verify all API endpoints work end-to-end
    - Verify Docker Compose deployment works
    - _Requirements: 1.x, 2.x, 3.x, 5.x, 6.x_
  
  - [ ] 12.2 Verify all requirements coverage
    - Confirm all acceptance criteria are covered by tests
    - Run property-based tests for all testable criteria
    - Run integration tests for API endpoints
    - _Requirements: All requirements_
  
  - [ ] 12.3 Final checkpoint - Ensure all tests pass
    - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional and can be skipped for faster MVP
- Each task references specific requirements for traceability
- Checkpoints ensure incremental validation
- Property-based tests validate universal correctness properties
- Unit tests validate specific examples and edge cases
- Implementation follows the layered architecture: Domain → Service → API → Frontend
- All design calculations include input validation (positive values required)
- All responses include metadata with timestamps and validation notices
- Docker Compose configuration supports development hot-reload
- Julia ODE solver uses Tsit5 integrator exclusively

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "2.1"] },
    { "id": 1, "tasks": ["1.4", "2.2", "2.3", "2.4", "2.5"] },
    { "id": 2, "tasks": ["2.6", "3.1", "3.2", "4.1", "4.2"] },
    { "id": 3, "tasks": ["3.3", "3.4", "4.3", "4.4", "4.5"] },
    { "id": 4, "tasks": ["3.5", "4.6", "5.1", "5.2", "6.1", "6.2", "6.3"] },
    { "id": 5, "tasks": ["5.3", "5.4", "6.4", "7.1", "7.2", "7.3", "7.4"] },
    { "id": 6, "tasks": ["7.5", "8.1", "8.2", "9.1", "9.2", "9.3"] },
    { "id": 7, "tasks": ["9.4", "9.5", "10.1", "10.2", "10.3", "12.1", "12.2"] },
    { "id": 8, "tasks": ["12.3"] }
  ]
}
```