from pydantic import BaseModel, Field

class ProcessUnit(BaseModel):
    id: str
    type: str
    name: str
    parameters: dict[str, float] = Field(default_factory=dict)
    states: dict[str, float] = Field(default_factory=dict)

    def parameter(self, key: str, default: float = 0.0) -> float:
        return float(self.parameters.get(key, default))
