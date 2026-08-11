from pydantic import BaseModel, Field
from app.domain.process_unit import ProcessUnit
from app.domain.stream import Stream

class PlantModel(BaseModel):
    id: str
    name: str
    units: list[ProcessUnit] = Field(default_factory=list)
    streams: list[Stream] = Field(default_factory=list)
    parameters: dict[str, float] = Field(default_factory=dict)
    metadata: dict = Field(default_factory=dict)

    def get_unit(self, unit_id: str) -> ProcessUnit:
        for unit in self.units:
            if unit.id == unit_id:
                return unit
        raise KeyError(f"Unidad no encontrada: {unit_id}")

    def upstream(self, unit_id: str) -> list[Stream]:
        return [s for s in self.streams if s.target == unit_id]

    def downstream(self, unit_id: str) -> list[Stream]:
        return [s for s in self.streams if s.source == unit_id]
