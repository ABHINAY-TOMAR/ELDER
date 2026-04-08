from typing import Dict, List, Literal, Optional, Any
from pydantic import BaseModel, Field, ConfigDict, field_validator


# --- INPUT MODELS ---

class RequirementInput(BaseModel):
    description: str = Field(..., description="Natural language description of the project")
    
class ReviewRequest(BaseModel):
    architecture_details: Dict[str, Any] = Field(..., description="Raw architecture details to critique")

class InteractionOption(BaseModel):
    id: str
    label: str
    recommended: bool = False

class PendingInteraction(BaseModel):
    field: str
    question: str
    options: List[InteractionOption]

class DispatchRequest(BaseModel):
    project_id: str = Field(..., description="Unique ID for the project")


# --- CORE DATA MODELS ---

class RequirementSpec(BaseModel):
    team_size: int = Field(default=1, description="Number of engineers")
    budget_usd: int = Field(default=0, description="Monthly or total budget")
    expected_users: int = Field(default=0, description="Expected users at launch")
    latency_requirement_ms: int = Field(default=500, description="p99 latency target")
    data_sensitivity: Literal["public", "internal", "pii"] = Field(default="public", description="Data sensitivity level")
    deployment_target: Literal["cloud", "on_prem", "hybrid"] = Field(default="cloud", description="Where this is deployed")
    timeline_weeks: int = Field(default=4, description="Target timeline")
    key_features: List[str] = Field(default_factory=list, description="Extracted key features")
    constraints: List[str] = Field(default_factory=list, description="Extracted constraints")
    
    model_config = ConfigDict(json_schema_extra={
        "example": {
            "team_size": 2,
            "budget_usd": 10000,
            "expected_users": 100000,
            "latency_requirement_ms": 500,
            "data_sensitivity": "pii",
            "deployment_target": "cloud",
            "timeline_weeks": 26,
            "key_features": ["recommendations", "real-time"],
            "constraints": ["must use AWS", "GDPR compliant"]
        }
    })

class Service(BaseModel):
    id: str = Field(..., description="Unique service ID (e.g. auth_service)")
    name: str = Field(..., description="Human-readable name")
    description: str = Field(..., description="What this service does")
    dependencies: List[str] = Field(default_factory=list, description="IDs of services this depends on")

class DependencyGraph(BaseModel):
    services: List[Service] = Field(..., description="Services in the format of a directed acyclic graph")

class DataFlow(BaseModel):
    producer: str = Field(..., description="Service ID that produces data")
    consumer: str = Field(..., description="Service ID that consumes data")
    sync_type: Literal["sync", "async"] = Field(..., description="Synchronous or asynchronous flow")
    format: str = Field(..., description="Data format (JSON, protobuf, etc.)")

class ADR(BaseModel):
    title: str = Field(..., description="Title of the decision")
    status: str = Field(default="Proposed", description="Status of the decision")
    context: str = Field(..., description="Context of why the decision is needed")
    decision: str = Field(..., description="What was chosen")
    rationale: str = Field(..., description="Why it was chosen over alternatives")

class FailureMode(BaseModel):
    mode: str = Field(..., description="Type of failure (e.g., service crash)")
    probability: Literal["high", "medium", "low"] = Field(..., description="Probability of occurrence")
    impact: str = Field(..., description="Impact description")
    detection_strategy: str = Field(..., description="How to detect")
    mitigation_strategy: str = Field(..., description="How to mitigate")
    fallback_strategy: str = Field(..., description="Fallback action")
    owner: str = Field(..., description="Owner or team managing this")
    severity: Literal["critical", "high", "medium", "low"] = Field(..., description="Severity level")


class RiskyDecision(BaseModel):
    id: str = Field(..., description="Unique ID for the risky decision")
    decision_type: str = Field(..., description="Type of decision (e.g., database_choice, security_model)")
    affected_component: str = Field(..., description="Which component this decision affects")
    reason: str = Field(..., description="Why this decision is risky")
    impact: Literal["high", "medium", "low"] = Field(..., description="Impact level")
    decision_context: str = Field(..., description="Context around this decision")
    why_needs_deep_thinking: str = Field(..., description="Why this needs extended reasoning")

class Phase(BaseModel):
    phase_number: int = Field(..., description="Index of the phase")
    name: str = Field(..., description="Name of the phase")
    services_to_build: List[str] = Field(..., description="Service IDs to implement")
    dependencies: List[int] = Field(default_factory=list, description="IDs of phases that must complete first")
    can_parallelize: bool = Field(..., description="If services within can go in parallel")
    priority: Literal["critical", "high", "medium"] = Field(..., description="Priority")
    duration_weeks: int = Field(..., description="Estimated effort in weeks")
    spec_text: str = Field(..., description="Markdown specification for developer")

class Recommendation(BaseModel):
    api_framework: str = Field(default="")
    database: str = Field(default="")
    cache_layer: str = Field(default="")
    message_queue: str = Field(default="")
    monitoring: str = Field(default="")
    vector_db: Optional[str] = Field(default=None)

class StackRecommendation(BaseModel):
    tech_stack: Recommendation = Field(..., description="Recommended technical stack")
    confidence: float = Field(..., description="Confidence score from 0.0 to 1.0")

class Architecture(BaseModel):
    project_id: str = Field(..., description="Unique project identifier")
    project_name: str = Field(..., description="Human-readable project name")
    domain: Literal["microservices", "ai_native", "data_pipeline"] = Field(..., description="Primary domain")
    services: List[Service] = Field(default_factory=list, description="List of services to build")
    tech_stack: Dict[str, str] = Field(default_factory=dict, description="Recommended technologies map")
    adrs: List[ADR] = Field(default_factory=list, description="Architectural decision records")
    failure_modes: Dict[str, List[FailureMode]] = Field(default_factory=dict, description="Identified risks by service id")
    data_flows: List[DataFlow] = Field(default_factory=list, description="Data movement specifications")
    implementation_phases: List[Phase] = Field(default_factory=list, description="Ordered phases")
    estimated_effort_weeks: int = Field(default=1, ge=1, le=52, description="Total effort")
    pending_interaction: Optional[PendingInteraction] = None

    def has_caching(self) -> bool:
        return "cache" in self.tech_stack.get("tech_stack", "").lower()
        
    def is_horizontally_scalable(self) -> bool:
        return True # Can be enriched based on specific tech stack analysis
        
    def has_encryption(self) -> bool:
        return True
        
    def has_monitoring(self) -> bool:
        return "monitoring" in self.tech_stack


# --- RESPONSE MODELS ---

class ArchitectureResponse(BaseModel):
    architecture: Architecture

class ReviewResponse(BaseModel):
    critique: str
    suggestions: List[str]

class DispatchResponse(BaseModel):
    task_id: str
    status: str

class StatusResponse(BaseModel):
    status: str
    progress: float

class ErrorResponse(BaseModel):
    error: str
    detail: str


# --- OPENENV-SPECIFIC MODELS ---

class TaskResetRequest(BaseModel):
    task_id: str

class TaskResetResponse(BaseModel):
    status: str

class TaskStepRequest(BaseModel):
    task_id: str
    action: Dict[str, Any]

class TaskStepResponse(BaseModel):
    observation: Dict[str, Any]
    reward: float
    done: bool

class TaskStatusResponse(BaseModel):
    task_id: str
    status: str

# --- DATABASE MODELS ---

class ProjectDB(BaseModel):
    id: str = Field(..., description="UUID")
    name: str = Field(...)
    created_at: str = Field(...)

class RequirementDB(BaseModel):
    project_id: str = Field(...)
    spec: RequirementSpec = Field(...)

class ArchitectureDB(BaseModel):
    project_id: str = Field(...)
    architecture: Architecture = Field(...)

class TaskAssignmentDB(BaseModel):
    task_id: str = Field(...)
    phase_number: int = Field(...)
    status: Literal["pending", "dispatched", "in_progress", "completed", "failed"] = Field(...)
    output_repo_url: Optional[str] = Field(default=None)
    validation_errors: Optional[List[str]] = Field(default=None)
    created_at: str = Field(...)
    completed_at: Optional[str] = Field(default=None)
