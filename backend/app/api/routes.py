from fastapi import APIRouter, HTTPException
from app.schemas import PlantRequest, SimulationRequest, ProcessUnitCalculationRequest, ProcessUnitCalculationResponse, ClassicPonderRequest, ClassicPonderResponse
from app.services.classic_service import build_demo_plant, design_plant, simulate_plant, calculate_unit
from app.calculations.classic_ponder import classic_ponder_calculation

router = APIRouter()

@router.get("/classic/demo")
def classic_demo():
    return build_demo_plant().model_dump()

@router.post("/classic/design")
def classic_design(request: PlantRequest):
    return design_plant(request.to_domain())

@router.post("/classic/simulate")
def classic_simulate(request: SimulationRequest):
    try:
        return simulate_plant(
            request.plant.to_domain(),
            request.duration_s,
            request.dt_s
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/classic/calculate-unit", response_model=ProcessUnitCalculationResponse)
def calculate_unit_endpoint(request: ProcessUnitCalculationRequest):
    """
    Calculate design or performance parameters for a specific process unit.
    """
    try:
        results = calculate_unit(
            request.unit_type,
            request.parameters,
            request.calculation_type
        )
        return ProcessUnitCalculationResponse(
            unit_id=request.unit_id,
            unit_type=request.unit_type,
            calculation_type=request.calculation_type,
            results=results,
            metadata={"calculation_timestamp": "2026-08-10T13:14:00Z"}
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

@router.post("/classic/ponder", response_model=ClassicPonderResponse)
def classic_ponder_endpoint(request: ClassicPonderRequest):
    """
    Perform classic ponder calculation for PTAP units with comprehensive validation and scoring.
    """
    try:
        result = classic_ponder_calculation(
            request.unit_type,
            request.parameters,
            request.calculation_type
        )
        return ClassicPonderResponse(
            unit_id=result.unit_id,
            unit_type=result.unit_type,
            calculation_type=result.calculation_type,
            ponder_value=result.ponder_value,
            variables_used=result.variables_used,
            formula=result.formula,
            validation_passed=result.validation_passed,
            warnings=result.warnings,
            metadata={
                "calculation_timestamp": "2026-08-10T13:14:00Z",
                "calculation_version": "1.0"
            }
        )
    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))
