import logging
import json
import os
import httpx
from typing import List, Dict, Any, Optional, Literal, Tuple
from pydantic import BaseModel, Field

from app.models.requirement_spec import RequirementSpec
from app.engines.fast_pattern_matcher import StackRecommendation, RiskyDecision
from app.core.token_tracker import ArchitectTokenTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DeepThought(BaseModel):
    decision_type: str
    original_recommendation: str
    refined_recommendation: str
    reasoning: str
    risk_mitigation: str

class FinalArchitectureRecommendation(BaseModel):
    tech_stack: Dict[str, str]
    deployment_target: str
    rationale: str
    risks_identified: List[RiskyDecision]
    deep_reasoning_applied: List[DeepThought] = Field(default_factory=list)
    confidence: float

class HybridReasoner:
    """
    Orchestrates the fast-path (rule-based) and deep-path (LLM-based) reasoning.
    """

    def __init__(self, token_tracker: Optional[ArchitectTokenTracker] = None):
        self.api_key = os.getenv("OPENAI_API_KEY") # We use OpenAI-compatible API for Claude if needed
        self.model = "gpt-4o" # Default for reasoning if not o1
        self.token_tracker = token_tracker

    async def reason(
        self, 
        spec: RequirementSpec, 
        fast_rec: StackRecommendation, 
        risky_decisions: List[RiskyDecision]
    ) -> FinalArchitectureRecommendation:
        """
        Merge fast-path recommendations with deep-path refinements for risky areas.
        """
        if not risky_decisions:
            logger.info(f"No risky decisions for {spec.project_name}. Returning fast recommendation.")
            return FinalArchitectureRecommendation(
                tech_stack=fast_rec.tech_stack,
                deployment_target=fast_rec.deployment_target,
                rationale=fast_rec.rationale,
                risks_identified=[],
                confidence=fast_rec.confidence
            )

        logger.info(f"Applying deep reasoning for {len(risky_decisions)} risks in {spec.project_name}...")
        
        deep_thoughts = []
        refined_stack = fast_rec.tech_stack.copy()
        
        # In a real implementation, we might batch these or do them in parallel
        for risk in risky_decisions:
            thought = await self._deep_think_on_risk(spec, fast_rec, risk)
            if thought:
                deep_thoughts.append(thought)
                # Update stack if LLM recommends a change
                # (Simple heuristic: if the refined_recommendation contains a known category)
                self._apply_refinement(refined_stack, thought)

        return FinalArchitectureRecommendation(
            tech_stack=refined_stack,
            deployment_target=fast_rec.deployment_target,
            rationale=f"{fast_rec.rationale} Refined with deep reasoning for {', '.join([r.decision_type for r in risky_decisions])}.",
            risks_identified=risky_decisions,
            deep_reasoning_applied=deep_thoughts,
            confidence=0.9 # Usually higher after deep reasoning
        )

    async def _deep_think_on_risk(
        self, 
        spec: RequirementSpec, 
        fast_rec: StackRecommendation, 
        risk: RiskyDecision
    ) -> Optional[DeepThought]:
        """
        Call LLM to evaluate a specific risky architectural decision.
        """
        if not self.api_key:
            return None

        prompt = f"""
        Project: {spec.project_name}
        Requirements: {spec.model_dump_json()}
        
        Proposed Stack: {json.dumps(fast_rec.tech_stack)}
        
        Specific Risk Detected:
        - Type: {risk.decision_type}
        - Reason: {risk.reason}
        - Why it needs deep thinking: {risk.why_needs_deep_thinking}
        
        Your task is to:
        1. Evaluate if the proposed stack effectively handles this risk.
        2. Propose a refined recommendation if the current one is insufficient.
        3. Explain your reasoning and mitigation strategy.
        
        Return the result as a JSON object matching this schema:
        {{
            "decision_type": "{risk.decision_type}",
            "original_recommendation": "the current tech for this category",
            "refined_recommendation": "new tech or 'same' if sufficient",
            "reasoning": "why",
            "risk_mitigation": "how to handle the risk"
        }}
        """

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={"Authorization": f"Bearer {self.api_key}"},
                    json={
                        "model": self.model,
                        "messages": [{"role": "user", "content": prompt}],
                        "response_format": {"type": "json_object"},
                        "temperature": 0.4
                    },
                    timeout=45.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Track usage
                if self.token_tracker:
                    usage = result.get("usage", {})
                    await self.token_tracker.track_usage(
                        project_id=spec.project_name,
                        model=self.model,
                        input_tokens=usage.get("prompt_tokens", 0),
                        output_tokens=usage.get("completion_tokens", 0),
                        reasoning_type="deep"
                    )

                content = json.loads(result["choices"][0]["message"]["content"])
                return DeepThought(**content)
            except Exception as e:
                logger.error(f"Deep thinking failed for {risk.decision_type}: {e}")
                return None

    def _apply_refinement(self, stack: Dict[str, str], thought: DeepThought):
        """Update the tech stack based on deep reasoning."""
        if thought.refined_recommendation.lower() == "same":
            return
            
        # Try to map decision_type to stack keys
        mapping = {
            "database": ["database", "vector_db"],
            "scaling": ["database", "cache", "message_queue"],
            "performance": ["api_framework", "cache"],
            "security": ["auth_provider", "api_framework"]
        }
        
        keys_to_update = mapping.get(thought.decision_type, [])
        for key in keys_to_update:
            if key in stack:
                stack[key] = thought.refined_recommendation
                break # Only update first match for simplicity
        else:
            # If no mapping, add as a new metadata key
            stack[f"refined_{thought.decision_type}"] = thought.refined_recommendation
