from pydantic import BaseModel, Field

class Stream(BaseModel):
    id: str
    source: str
    target: str
    flow_m3_s: float = 0.0
    quality: dict[str, float] = Field(default_factory=dict)
