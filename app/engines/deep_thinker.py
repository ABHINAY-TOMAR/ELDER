import json
import structlog
from typing import List, Dict, Any
from app.engines.llm_client import call_llm
from app.core.token_tracker import ArchitectTokenTracker

logger = structlog.get_logger("architect_agent.deep_thinker")

class DeepThinker:
    """
    Implements multi-hypothesis reasoning patterns derived from Open Deep Research.
    Used for rigorously evaluating risky architectural decisions.
    """
    
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.tracker = ArchitectTokenTracker()
        
    def _score_evaluation(self, eval_text: str) -> float:
        # Simple heuristic to extract a score from the LLM summary, or fallback.
        # Open Deep Research parses out self-assessment scores.
        # If the LLM generates "Score: 8/10", we extract 8.
        try:
            if "Score:" in eval_text:
                parts = eval_text.split("Score:")
                if len(parts) > 1:
                    score_str = parts[1].split()[0].replace("/10", "").replace(',', '').strip()
                    return float(score_str)
        except Exception:
            pass
        return 5.0 # default neutral

    async def evaluate_alternatives(
        self,
        decision_type: str,
        alternatives: List[str],
        constraints: Dict[str, Any],
        model: str = "claude-3-5-sonnet-20241022" 
    ) -> Dict[str, Any]:
        logger.info("deep_thinker_start", decision_type=decision_type, alternatives=len(alternatives))
        
        hypotheses = []
        for alt in alternatives:
            hypothesis = f"""
            Using {alt} for {decision_type}.
            Evaluate based on:
            - Trade-offs (Pros/Cons)
            - Risk of failure / SPOF
            - Team Skill fit (Constraints provided: {json.dumps(constraints)})
            - Latency and Scale implications
            """
            hypotheses.append({
                "alternative": alt,
                "hypothesis": hypothesis
            })
            
        evaluations = []
        for h in hypotheses:
            system_prompt = "You are an expert system architect performing deep analysis on a specific hypothesis. Conclude with 'Score: X/10'."
            user_prompt = h["hypothesis"]
            
            # Using call_llm directly
            # In a real "extended thinking" platform, we'd pass thinking=True (o1 or claude extended)
            # For now, we simulate the deep think by asking it to reason step by step.
            response_text = await call_llm(
                system_prompt=system_prompt,
                user_prompt=user_prompt + "\nReason step-by-step.",
                model=model,
                max_tokens=4000
            )
            
            # Rough token estimate (in a real system we'd get this from the API response)
            approx_input_tokens = len(system_prompt + user_prompt) // 4
            approx_output_tokens = len(response_text) // 4
            
            await self.tracker.track_usage(
                project_id=self.project_id,
                model=model,
                input_tokens=approx_input_tokens,
                output_tokens=approx_output_tokens,
                reasoning_type="deep"
            )
            
            evaluations.append({
                "alternative": h["alternative"],
                "evaluation": response_text,
                "score": self._score_evaluation(response_text)
            })
            
        # Synthesize: pick best
        if not evaluations:
            return {"chosen": None}
            
        best = max(evaluations, key=lambda e: e["score"])
        
        logger.info("deep_thinker_complete", chosen=best["alternative"], score=best["score"])
        
        return {
            "chosen": best["alternative"],
            "alternatives_considered": [e["alternative"] for e in evaluations],
            "reasoning": best["evaluation"],
            "all_evaluations": evaluations
        }
