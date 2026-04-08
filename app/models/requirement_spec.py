from typing import List, Literal, Dict, Optional
from pydantic import BaseModel, Field

class RequirementSpec(BaseModel):
    """
    Structured specification extracted from natural language requirements.
    This model serves as the input to all downstream reasoning engines.
    """
    project_name: str = Field(..., description="The name of the project being designed.")
    
    domain: Literal["microservices", "ai_native", "data_pipeline", "hybrid"] = Field(
        default="microservices", 
        description="The architectural domain of the system."
    )
    
    team_size: int = Field(default=2, description="Number of engineers on the team.")
    budget_usd: int = Field(default=5000, description="Available budget for the project/infrastructure.")
    
    expected_users: int = Field(default=1000, description="Projected number of concurrent or total users.")
    latency_requirement_ms: int = Field(default=500, description="Target end-to-end latency in milliseconds.")
    
    data_sensitivity: Literal["public", "internal", "pii", "regulated"] = Field(
        default="internal", 
        description="Sensitivity of the data being handled (affects security architecture)."
    )
    
    deployment_target: Literal["cloud", "on_prem", "hybrid", "edge"] = Field(
        default="cloud", 
        description="Target deployment environment."
    )
    
    constraints: List[str] = Field(
        default_factory=list, 
        description="Explicit hard constraints (e.g., 'must use AWS', 'team knows Node.js')."
    )
    
    timeline_weeks: int = Field(default=4, description="Target timeline for MVP implementation.")
    
    extracted_features: List[str] = Field(
        default_factory=list, 
        description="Core features identified from the requirement text."
    )

    class Config:
        json_schema_extra = {
            "example": {
                "project_name": "EduCore",
                "domain": "microservices",
                "team_size": 3,
                "budget_usd": 10000,
                "expected_users": 50000,
                "latency_requirement_ms": 200,
                "data_sensitivity": "pii",
                "deployment_target": "cloud",
                "constraints": ["Must use PostgreSQL", "Serverless preferred"],
                "timeline_weeks": 8,
                "extracted_features": ["User Authentication", "Real-time Chat", "Quiz Engine"]
            }
        }
