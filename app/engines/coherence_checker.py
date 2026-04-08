import structlog
from typing import List, Dict, Tuple, Literal
from pydantic import BaseModel
from app.models.schemas import Architecture

logger = structlog.get_logger("architect_agent.coherence_checker")

class CoherenceIssue(BaseModel):
    type: Literal["api_mismatch", "schema_mismatch", "message_mismatch", "naming"]
    severity: Literal["critical", "high", "medium", "low"]
    services_affected: List[str]
    description: str
    suggested_fix: str

class CoherenceCheckResult(BaseModel):
    passed: bool
    issues: List[CoherenceIssue]
    warnings: List[str]
    integration_score: float  # 0.0-1.0
    affected_service_pairs: List[Tuple[str, str]]
    recommendation: str

class DispatchResult(BaseModel):
    task_id: str
    status: str
    output_repo: str = ""
    validation_errors: List[str] = []

async def check_coherence(
    phase_outputs: List[DispatchResult],
    architecture: Architecture
) -> CoherenceCheckResult:
    """
    Validates that the generated services interoperate based on API contracts and schema matching.
    Currently acts as a mock/stub since real code requires repository cloning and parsing.
    """
    logger.info("coherence_check_start", total_outputs=len(phase_outputs))
    
    issues: List[CoherenceIssue] = []
    affected_pairs: List[Tuple[str, str]] = []
    
    # Check 4: Naming conventions (simulate some static checks on metadata if present)
    naming_issues = check_naming_conventions(phase_outputs)
    issues.extend(naming_issues)
    
    # Future Check 1, 2, 3 logic will parse OpenAPI YAMLs locally
    score = 1.0
    passed = True
    
    if len(issues) > 0:
        score = 0.8
        passed = False
        
    res = CoherenceCheckResult(
        passed=passed,
        issues=issues,
        warnings=["Full AST/OpenAPI parsing requires codebase cloning."],
        integration_score=score,
        affected_service_pairs=affected_pairs,
        recommendation="Review all naming patterns and ensure API boundaries align."
    )
    
    logger.info("coherence_check_complete", score=score, passed=passed)
    return res

def check_naming_conventions(outputs: List[DispatchResult]) -> List[CoherenceIssue]:
    # Placeholder for checking code repository files for snake_case/kebab-case.
    return []
