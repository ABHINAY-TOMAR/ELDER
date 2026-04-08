import json
import structlog
from typing import List, Dict, Any
from app.engines.llm_client import call_llm
from app.core.token_tracker import ArchitectTokenTracker

logger = structlog.get_logger("architect_agent.tech_research")

class TechResearchLoop:
    """
    Implements iterative refinement loops derived from Auto Research Claw.
    Used for verifying technology choices against specific constraints iteratively.
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.tracker = ArchitectTokenTracker()

    def _is_converged(self, findings: List[str]) -> bool:
        # A simple convergence check: if the latest finding explicitly says "CONVERGED"
        if findings and "CONVERGED" in findings[-1]:
            return True
        return False

    async def _evaluate_alternative(self, alternatives: List[str], constraints: Dict, previous_findings: List[str], model: str) -> str:
        sys_prompt = "You are an iterative research assistant. Evaluate the following alternatives against the constraints. Consider previous findings. If a clear winner emerges that satisfies all constraints, end your response with 'CONVERGED'."
        user_prompt = f"Alternatives: {json.dumps(alternatives)}\nConstraints: {json.dumps(constraints)}\nPrevious findings: {json.dumps(previous_findings)}"
        
        res = await call_llm(
            system_prompt=sys_prompt,
            user_prompt=user_prompt,
            model=model,
            max_tokens=2000
        )
        
        # Track Tokens
        in_tokens = len(sys_prompt + user_prompt) // 4
        out_tokens = len(res) // 4
        await self.tracker.track_usage(self.project_id, model, in_tokens, out_tokens, "deep")
        
        return res

    async def _refine_alternatives(self, current_alts: List[str], finding: str) -> List[str]:
        # Dummy refinement: just filter out clearly rejected ones parsing 'reject XYZ'
        refined = []
        for alt in current_alts:
            if f"reject {alt.lower()}" not in finding.lower() and f"eliminate {alt.lower()}" not in finding.lower():
                refined.append(alt)
        return refined if refined else current_alts # fallback to original if all rejected

    async def research_tech_choice(
        self,
        decision_type: str,
        constraints: Dict[str, Any],
        initial_alternatives: List[str],
        max_iterations: int = 3,
        model: str = "claude-3-5-sonnet-20241022"
    ) -> Dict[str, Any]:
        """Iterative loop evaluating a specific technology choice."""
        logger.info("tech_research_start", decision_type=decision_type)
        
        findings = []
        current_alternatives = initial_alternatives.copy()
        
        for iteration in range(max_iterations):
            logger.info("tech_research_iteration", iteration=iteration+1, alternatives=current_alternatives)
            
            # Evaluate current alternatives
            finding = await self._evaluate_alternative(current_alternatives, constraints, findings, model)
            findings.append(finding)
            
            if self._is_converged(findings):
                logger.info("tech_research_converged")
                break
                
            # Refine alternatives
            current_alternatives = await self._refine_alternatives(current_alternatives, finding)
            
        sys_synthesis = "Synthesize these research findings into a final choice and a short reasoning block."
        user_synthesis = f"Decision Type: {decision_type}\nFindings: {json.dumps(findings)}\nFinal Alternatives left: {current_alternatives}"
        
        final_synth = await call_llm(sys_synthesis, user_synthesis, model=model, max_tokens=1000)
        
        # Track synthesis
        in_tokens = len(sys_synthesis + user_synthesis) // 4
        out_tokens = len(final_synth) // 4
        await self.tracker.track_usage(self.project_id, model, in_tokens, out_tokens, "deep")
        
        # Rough parse
        chosen = current_alternatives[0] if current_alternatives else initial_alternatives[0]
        
        return {
            "chosen": chosen,
            "alternatives_rejected": list(set(initial_alternatives) - set(current_alternatives)),
            "reasoning": final_synth
        }
