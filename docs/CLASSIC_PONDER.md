# Classic Ponder Module for PTAP Calculations

## Overview

The Classic Ponder Module provides comprehensive calculation and validation functions for water treatment plant (PTAP) process units. It implements industry-standard formulas for hydraulic calculations, efficiency scoring, and performance evaluation.

## Features

- **Input Validation**: Comprehensive validation of input parameters with warning system
- **Design Calculations**: Standard hydraulic and process calculations for all unit types
- **Performance Evaluation**: Efficiency scoring based on industry standards
- **Error Handling**: Robust error handling with detailed error messages
- **Flexible API**: Support for different calculation types (design, performance, efficiency)

## Supported Unit Types

### 1. Rapid Mix
- **Parameters**: Q_m3_s, volume_m3, G_s, coagulant_mg_l
- **Calculations**: Detention time, mixing energy, power requirements
- **Efficiency**: Based on velocity gradient (optimal: 500-1000 s⁻¹)

### 2. Flocculation
- **Parameters**: Q_m3_s, volume_m3, G_s
- **Calculations**: Detention time, Gt value
- **Efficiency**: Based on Gt value (optimal: 20,000-100,000)

### 3. Sedimentation
- **Parameters**: Q_m3_s, area_m2, depth_m
- **Calculations**: Surface overflow rate, hydraulic loading rate, detention time
- **Efficiency**: Based on surface overflow rate (lower is better)

### 4. Filtration
- **Parameters**: Q_m3_s, area_m2
- **Calculations**: Filtration rate
- **Efficiency**: Based on filtration rate (optimal: 5-15 m³/m²/h)

### 5. Disinfection
- **Parameters**: Q_m3_s, volume_m3, chlorine_mg_l
- **Calculations**: Contact time, CT value
- **Efficiency**: Based on CT value for virus inactivation

## API Usage

### Classic Ponder Calculation

**Endpoint**: `POST /classic/ponder`

**Request**:
```json
{
  "unit_id": "sedimentation_1",
  "unit_type": "sedimentation",
  "parameters": {
    "Q_m3_s": 0.5,
    "area_m2": 1500,
    "depth_m": 4
  },
  "calculation_type": "design"
}
```

**Response**:
```json
{
  "unit_id": "sedimentation_1",
  "unit_type": "sedimentation",
  "calculation_type": "design",
  "ponder_value": 45.67,
  "variables_used": {
    "Q_m3_s": 0.5,
    "area_m2": 1500,
    "depth_m": 4
  },
  "formula": "V = A·h, SOR = Q/A·3600, HLR = Q/A·86400",
  "validation_passed": true,
  "warnings": [],
  "metadata": {
    "calculation_timestamp": "2026-08-10T13:14:00Z",
    "calculation_version": "1.0"
  }
}
```

## Calculation Types

### Design Calculations
Provide standard hydraulic and process calculations based on unit parameters.

**Example - Sedimentation Design**:
```python
result = classic_ponder_calculation(
    unit_type="sedimentation",
    parameters={
        "Q_m3_s": 0.5,
        "area_m2": 1500,
        "depth_m": 4
    },
    calculation_type="design"
)
```

**Results Include**:
- Surface overflow rate (m³/m²/h)
- Hydraulic loading rate (m³/m²/day)
- Volume (m³)
- Detention time (h)

### Performance Calculations
Evaluate unit performance based on operational parameters.

**Example - Filtration Performance**:
```python
result = classic_ponder_calculation(
    unit_type="filtration",
    parameters={
        "Q_m3_s": 0.5,
        "area_m2": 250
    },
    calculation_type="performance"
)
```

**Results Include**:
- Filtration rate (m³/m²/h)
- Efficiency score (0-100)
- Turbidity removal percentage

### Efficiency Calculations
Comprehensive efficiency scoring based on industry standards.

**Example - Disinfection Efficiency**:
```python
result = classic_ponder_calculation(
    unit_type="disinfection",
    parameters={
        "Q_m3_s": 0.5,
        "volume_m3": 900,
        "chlorine_mg_l": 1.5
    },
    calculation_type="efficiency"
)
```

**Results Include**:
- CT value (mg·min/L)
- Log inactivation
- Efficiency score (0-100)

## Input Validation

The module includes comprehensive input validation with the following checks:

### Flow Rate (Q_m3_s)
- Must be positive (> 0)
- Warning if > 10 m³/s (unusually high)

### Volume (volume_m3)
- Must be positive (> 0)
- Warning if > 50,000 m³ (unusually high)

### Area (area_m2)
- Must be positive (> 0)
- Warning if > 100,000 m² (unusually high)

### Depth (depth_m)
- Must be positive (> 0)
- Warning if > 20 m (unusually high)

### Velocity Gradient (G_s)
- Must be positive (> 0)
- Warning if > 1000 s⁻¹ (unusually high)

### Chemical Dosages
- Coagulant: 0-200 mg/L (warning if > 200 mg/L)
- Chlorine: 0-10 mg/L (warning if > 10 mg/L)

### Water Quality
- Turbidity: 0-1000 NTU (warning if > 1000 NTU)
- pH: 0-14 (error if outside range)

## Formulas Used

### Hydraulic Loading Rate
```
HLR = (Q × 86400) / A
```
Where:
- HLR = Hydraulic loading rate (m³/m²/day)
- Q = Flow rate (m³/s)
- A = Surface area (m²)

### Surface Overflow Rate
```
SOR = (Q × 3600) / A
```
Where:
- SOR = Surface overflow rate (m³/m²/h)
- Q = Flow rate (m³/s)
- A = Surface area (m²)

### Detention Time
```
t = V / Q / 3600
```
Where:
- t = Detention time (hours)
- V = Volume (m³)
- Q = Flow rate (m³/s)

### Mixing Energy
```
P = μ × G² × V
```
Where:
- P = Power (watts)
- μ = Dynamic viscosity (Pa·s)
- G = Velocity gradient (s⁻¹)
- V = Volume (m³)

### Floculation Efficiency (Gt Value)
```
Gt = G × t × 3600
```
Where:
- Gt = Dimensionless floculation parameter
- G = Velocity gradient (s⁻¹)
- t = Detention time (hours)

### Filtration Rate
```
FR = (Q × 3600) / A
```
Where:
- FR = Filtration rate (m³/m²/h)
- Q = Flow rate (m³/s)
- A = Filter area (m²)

### Disinfection Contact Time
```
t = V / Q / 60
```
Where:
- t = Contact time (minutes)
- V = Disinfection chamber volume (m³)
- Q = Flow rate (m³/s)

### CT Value
```
CT = C × t
```
Where:
- CT = CT value (mg·min/L)
- C = Chlorine concentration (mg/L)
- t = Contact time (minutes)

## Error Handling

The module provides comprehensive error handling:

1. **Input Validation Errors**: Detailed warnings for out-of-range values
2. **Calculation Errors**: Clear error messages for invalid calculations
3. **Unit Type Errors**: Support validation for supported unit types
4. **Calculation Type Errors**: Validation for supported calculation types

## Testing

Run the test suite:
```bash
cd backend
python -m pytest tests/test_classic_ponder.py -v
```

The test suite includes:
- Input validation tests
- Hydraulic calculation tests
- Efficiency calculation tests
- Error handling tests
- Edge case tests

## Integration

The Classic Ponder Module integrates with the existing Yaku Digital Twin framework:

1. **API Integration**: Added to `/classic/ponder` endpoint
2. **Schema Integration**: New request/response models defined
3. **Service Integration**: Available through classic_service.py
4. **Domain Integration**: Compatible with existing PlantModel and ProcessUnit classes

## Performance Considerations

- All calculations are O(1) complexity
- Validation is performed before calculations
- Memory efficient with minimal overhead
- Supports batch processing through API endpoints

## Future Enhancements

1. **Additional Unit Types**: Support for advanced treatment processes
2. **Temperature Corrections**: Temperature-dependent calculations
3. **Water Quality Modeling**: Integrated water quality simulations
4. **Machine Learning**: AI-based efficiency optimization
5. **Real-time Monitoring**: Integration with sensor data

## References

- Standard Methods for the Examination of Water and Wastewater
- AWWA Water Treatment Plant Design
- EPA Guidance Manual for Conventional Filtration
- WHO Guidelines for Drinking-water Quality