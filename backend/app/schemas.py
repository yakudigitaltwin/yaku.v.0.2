from typing import Any
from pydantic import BaseModel, Field
from app.domain.plant import PlantModel
from app.domain.process_unit import ProcessUnit
from app.domain.stream import Stream

class UnitRequest(BaseModel):
    id: str
    type: str
    name: str
    parameters: dict[str, float] = Field(default_factory=dict)

class StreamRequest(BaseModel):
    id: str
    source: str
    target: str
    flow_m3_s: float = 0.0
    quality: dict[str, float] = Field(default_factory=dict)

class PlantRequest(BaseModel):
    id: str = "ptap-demo"
    name: str = "Yaku PTAP Demo"
    units: list[UnitRequest]
    streams: list[StreamRequest] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

    def to_domain(self) -> PlantModel:
        return PlantModel(
            id=self.id,
            name=self.name,
            units=[
                ProcessUnit(id=u.id, type=u.type, name=u.name, parameters=u.parameters)
                for u in self.units
            ],
            streams=[
                Stream(
                    id=s.id, source=s.source, target=s.target,
                    flow_m3_s=s.flow_m3_s, quality=s.quality
                )
                for s in self.streams
            ],
            metadata=self.metadata
        )

class ProcessUnitCalculationRequest(BaseModel):
    unit_id: str
    unit_type: str
    parameters: dict[str, float] = Field(default_factory=dict)
    calculation_type: str = "design"  # "design" or "performance"

class ProcessUnitCalculationResponse(BaseModel):
    unit_id: str
    unit_type: str
    calculation_type: str
    results: dict[str, float]
    metadata: dict[str, Any] = Field(default_factory=dict)

class ClassicPonderRequest(BaseModel):
    unit_id: str
    unit_type: str
    parameters: dict[str, float] = Field(default_factory=dict)
    calculation_type: str = "design"  # "design", "performance", or "efficiency"

class ClassicPonderResponse(BaseModel):
    unit_id: str
    unit_type: str
    calculation_type: str
    ponder_value: float
    variables_used: dict[str, float]
    formula: str
    validation_passed: bool
    warnings: list[str] = Field(default_factory=list)
    metadata: dict[str, Any] = Field(default_factory=dict)

class SimulationRequest(BaseModel):
    plant: PlantRequest
    duration_s: float = Field(3600.0, gt=0, le=86400)
    dt_s: float = Field(10.0, gt=0, le=3600)
