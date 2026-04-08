from typing import List, Dict, Any, Optional, Literal
from pydantic import BaseModel, Field

class Service(BaseModel):
    id: str
    name: str
    description: str
    stack: str
    dependencies: List[str] = Field(default_factory=list)
    endpoints: List[str] = Field(default_factory=list)

class ADR(BaseModel):
    title: str
    context: str
    decision: str
    alternatives: List[str] = Field(default_factory=list)
    consequences: str

class FailureMode(BaseModel):
    service_id: str
    mode: str
    probability: Literal["high", "medium", "low"]
    impact: str
    detection: str
    mitigation: str

class Phase(BaseModel):
    phase_number: int
    name: str
    service_ids: List[str]
    description: str
    dependencies: List[int] = Field(default_factory=list) # phase numbers
    spec_markdown: Optional[str] = None

class Architecture(BaseModel):
    project_id: str
    project_name: str
    domain: str
    tech_stack: Dict[str, str]
    services: List[Service]
    adrs: List[ADR] = Field(default_factory=list)
    failure_modes: List[FailureMode] = Field(default_factory=list)
    phases: List[Phase] = Field(default_factory=list)
    estimated_effort_weeks: int = Field(default=4, ge=1)
    rationale: str
