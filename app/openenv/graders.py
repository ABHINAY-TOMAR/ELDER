import logging
from typing import Dict, List, Any
from app.models.architecture import Architecture

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def fuzzy_match(val: str, truth: str) -> float:
    """Simple keyword-based similarity."""
    val = val.lower().strip()
    truth = truth.lower().strip()
    if val == truth: return 1.0
    if val in truth or truth in val: return 0.8
    return 0.0

class OpenEnvGraders:
    """
    Deterministic graders for OpenEnv tasks.
    """

    def grade_tech_stack(self, agent_rec: Dict[str, str], ground_truth: Dict[str, str]) -> float:
        """Task 1: How well does the recommended stack match the expert truth?"""
        score = 0.0
        keys = ["api_framework", "database", "cache", "message_queue"]
        
        for key in keys:
            val = agent_rec.get(key, "none")
            truth = ground_truth.get(key, "none")
            score += fuzzy_match(val, truth)
            
        return score / len(keys)

    def grade_anti_patterns(self, agent_findings: List[str], ground_truth: List[str]) -> float:
        """Task 2: % of injected anti-patterns correctly identified."""
        if not ground_truth: return 1.0
        
        found_count = 0
        findings_str = " ".join(agent_findings).lower()
        
        for pattern in ground_truth:
            if pattern.lower() in findings_str:
                found_count += 1
                
        return found_count / len(ground_truth)

    def grade_full_design(self, arch: Architecture, ground_truth_reqs: Dict[str, Any]) -> float:
        """Task 3: Composite score for full design integration."""
        # 1. Sensibility (Does it have a DB and API?)
        sensibility = 0.0
        if arch.services and any("database" in str(s.stack).lower() for s in arch.services):
            sensibility += 0.5
        if any("api" in str(s.name).lower() for s in arch.services):
            sensibility += 0.5
            
        # 2. Decomposition (Service count)
        service_count = len(arch.services)
        decomposition = 1.0 if 2 <= service_count <= 8 else 0.5
        
        # 3. Integration (Are there dependencies?)
        integration = 1.0 if any(s.dependencies for s in arch.services) else 0.0
        
        return (sensibility * 0.4) + (decomposition * 0.3) + (integration * 0.3)
