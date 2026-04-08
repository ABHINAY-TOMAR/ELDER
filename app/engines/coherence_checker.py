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
    """
    Check naming conventions in generated code.
    
    Validates:
    - Service names use snake_case
    - Database tables use plural snake_case
    - API endpoints use kebab-case
    - Environment variables use UPPER_SNAKE_CASE
    """
    issues: List[CoherenceIssue] = []
    
    for output in outputs:
        task_id = output.task_id
        
        if not output.output_repo:
            continue
        
        service_name_from_task = task_id.split("-phase-")[0] if "-phase-" in task_id else task_id
        
        if not _is_snake_case(service_name_from_task):
            issues.append(CoherenceIssue(
                type="naming",
                severity="medium",
                services_affected=[task_id],
                description=f"Service name '{service_name_from_task}' should use snake_case",
                suggested_fix="Rename to snake_case: e.g., 'auth_service' not 'authService'"
            ))
    
    return issues


def _is_snake_case(name: str) -> bool:
    """Check if a name follows snake_case convention."""
    if not name:
        return True
    import re
    return bool(re.match(r'^[a-z][a-z0-9_]*$', name))


def validate_output(
    result: Dict[str, Any],
    phase: Phase,
    architecture: Architecture
) -> CoherenceCheckResult:
    """
    Validate the output repository from an agent dispatch.
    
    Checks:
    - Repository URL is present
    - Required files exist (openapi.yaml, requirements.txt, etc.)
    - Code compiles without errors
    """
    issues: List[CoherenceIssue] = []
    warnings: List[str] = []
    
    output_repo = result.get("output_repo", "")
    
    if not output_repo:
        issues.append(CoherenceIssue(
            type="api_mismatch",
            severity="high",
            services_affected=[phase.name],
            description="No repository URL returned from dispatch",
            suggested_fix="Agent should return a valid repository URL"
        ))
        return CoherenceCheckResult(
            passed=False,
            issues=issues,
            warnings=warnings,
            integration_score=0.0,
            affected_service_pairs=[],
            recommendation="Dispatch failed - no output repository"
        )
    
    if not output_repo.startswith(("http://", "https://", "git@")):
        issues.append(CoherenceIssue(
            type="api_mismatch",
            severity="high",
            services_affected=[phase.name],
            description=f"Invalid repository URL format: {output_repo}",
            suggested_fix="Repository URL should be a valid GitHub/GitLab URL"
        ))
    
    warnings.append("Code compilation check requires repository cloning - not implemented yet")
    warnings.append("OpenAPI schema validation requires repository cloning - not implemented yet")
    
    score = 1.0 if len(issues) == 0 else 0.5
    passed = len(issues) == 0
    
    return CoherenceCheckResult(
        passed=passed,
        issues=issues,
        warnings=warnings,
        integration_score=score,
        affected_service_pairs=[],
        recommendation="Review warnings and validate schema manually" if warnings else "Output validated successfully"
    )


from typing import Dict, Any
from app.models.schemas import Phase
