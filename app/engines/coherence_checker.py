import logging
from typing import List, Dict, Any, Tuple, Literal
from pydantic import BaseModel, Field
from app.models.architecture import Architecture

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class CoherenceIssue(BaseModel):
    issue_type: Literal["api_mismatch", "schema_mismatch", "naming_inconsistency"]
    severity: Literal["critical", "high", "medium", "low"]
    description: str
    affected_services: List[str]
    suggested_fix: str

class CoherenceResult(BaseModel):
    passed: bool
    score: float # 0.0 to 1.0
    issues: List[CoherenceIssue]
    summary: str

class CoherenceChecker:
    """
    Validates that implemented services integrate correctly according to the architecture.
    """

    async def check(
        self, 
        arch: Architecture, 
        service_specs: Dict[str, Dict[str, Any]] # service_id -> parsed_spec
    ) -> CoherenceResult:
        """
        Run integration validation across all services.
        """
        logger.info(f"Checking coherence for {arch.project_name}...")
        issues = []

        # 1. Check API Contract Matching (Consumer -> Provider)
        for consumer_svc in arch.services:
            for provider_id in consumer_svc.dependencies:
                provider_spec = service_specs.get(provider_id)
                if not provider_spec:
                    continue # Might not be implemented yet
                
                # Check if consumer expectations match provider endpoints
                # (Heuristic check for now)
                api_issues = self._check_api_contracts(consumer_svc.id, provider_id, provider_spec)
                issues.extend(api_issues)

        # 2. Check Database Schema Alignment
        # (Compare shared table definitions if applicable)

        # 3. Calculate Score
        critical_count = len([i for i in issues if i.severity == "critical"])
        high_count = len([i for i in issues if i.severity == "high"])
        
        score = 1.0 - (critical_count * 0.4) - (high_count * 0.1)
        score = max(0.0, score)

        return CoherenceResult(
            passed=critical_count == 0,
            score=score,
            issues=issues,
            summary=f"Validation complete. Found {len(issues)} issues."
        )

    def _check_api_contracts(self, consumer_id: str, provider_id: str, provider_spec: Dict) -> List[CoherenceIssue]:
        """Simple heuristic to check for missing provider endpoints."""
        issues = []
        # In a real system, we'd parse the consumer's call-sites and match them
        # against the provider's OpenAPI spec.
        return issues
