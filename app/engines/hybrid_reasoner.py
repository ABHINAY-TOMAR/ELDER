import os
import json
import structlog
from typing import Dict, Any, List

from app.models.schemas import RequirementSpec, RiskyDecision, Architecture
from app.engines.llm_client import call_llm
from app.engines.model_selector import ModelSelector, ModelComplexity
from app.core.token_tracker import ArchitectTokenTracker
from app.engines.deep_thinker import DeepThinker
from app.engines.tech_research import TechResearchLoop

logger = structlog.get_logger("architect_agent.hybrid_reasoner")

class HybridReasoner:
    """
    Integrates fast pattern recommendation, risk detection, TokenTracker,
    ModelSelector, DeepThinker, and TechResearchLoop to finalize tech choices.
    """
    def __init__(self, project_id: str):
        self.project_id = project_id
        self.model_selector = ModelSelector()
        self.tracker = ArchitectTokenTracker()
        self.deep_thinker = DeepThinker(project_id)
        self.research_loop = TechResearchLoop(project_id)

    async def evaluate_risky_decisions(
        self,
        spec: RequirementSpec,
        fast_rec: Dict[str, str],
        risky_decisions: List[RiskyDecision]
    ) -> Dict[str, str]:
        """
        Evaluate all risky decisions utilizing appropriate depth and models.
        """
        if not risky_decisions:
            logger.info("no_risky_decisions_using_fast_path")
            
            # Log Fast path Token Usage explicitly
            await self.tracker.track_usage(
                project_id=self.project_id,
                model="claude-3-5-haiku-20241022",
                input_tokens=1000,   # Approx estimate of fast context
                output_tokens=200,   # Approx map 
                reasoning_type="fast"
            )
            return fast_rec

        # Fetch current project costs to inform ModelSelector budget
        cost_summary = await self.tracker.get_project_total_cost(self.project_id)
        budget_remaining = spec.budget_usd - float(cost_summary.get("total_cost", 0.0))
        
        refined_rec = dict(fast_rec)

        for decision in risky_decisions:
            logger.info("evaluating_risky_decision", decision_id=decision.id, impact=decision.impact)
            
            # Map impact string to enum
            complexity = ModelComplexity.MEDIUM
            if decision.impact.lower() == "high":
                complexity = ModelComplexity.HIGH
            elif decision.impact.lower() == "low":
                complexity = ModelComplexity.LOW
                
            model = await self.model_selector.select_model(
                complexity=complexity,
                budget_remaining=budget_remaining,
                use_extended_thinking=(complexity == ModelComplexity.HIGH)
            )
            
            logger.info("selected_model_for_decision", model=model, complexity=complexity)
            
            # If High Impact, use DeepThinker
            if complexity == ModelComplexity.HIGH:
                # We need some alternatives. We can generate them quickly or hardcode common ones
                alternatives = [decision.affected_component]
                # Fallbacks depending on type
                if "db" in decision.affected_component.lower() or "database" in decision.decision_context.lower():
                    alternatives.extend(["PostgreSQL", "Cassandra", "MongoDB"])
                elif "cache" in decision.affected_component.lower():
                    alternatives.extend(["Redis Cluster", "Memcached"])
                else:
                    alternatives.extend(["Standard Implementation", "Custom Vendor Solution"])
                
                result = await self.deep_thinker.evaluate_alternatives(
                    decision_type=decision.affected_component,
                    alternatives=list(set(alternatives)), # unique
                    constraints={"context": decision.decision_context},
                    model=model
                )
                
                if result["chosen"]:
                    refined_rec[decision.affected_component] = result["chosen"]
                    
            # If Medium, use Iterative Research Loop
            elif complexity == ModelComplexity.MEDIUM:
                alternatives = [decision.affected_component, "Alternative A", "Alternative B"]
                
                result = await self.research_loop.research_tech_choice(
                    decision_type=decision.affected_component,
                    constraints={"context": decision.decision_context},
                    initial_alternatives=alternatives,
                    model=model
                )
                
                if result["chosen"]:
                    refined_rec[decision.affected_component] = result["chosen"]
            else:
                # Low impact but flagged: do a fast direct LLM resolution
                sys_prompt = "You are an architect. Adjust the technical choice given the following risk."
                usr_prompt = f"Component: {decision.affected_component}\nRisk Context: {decision.decision_context}\nCurrent: {fast_rec.get(decision.affected_component, 'unknown')}\nReply only with the best technology name."
                
                res = await call_llm(sys_prompt, usr_prompt, model=model, max_tokens=100)
                refined_rec[decision.affected_component] = res.strip()
                
                await self.tracker.track_usage(
                    self.project_id, model, in_tokens=len(usr_prompt)//4, output_tokens=10, reasoning_type="fast"
                )

        return refined_rec

    async def merge_and_finalize(
        self,
        spec: RequirementSpec,
        risky_decisions: List[RiskyDecision],
        refined_tech_stack: Dict[str, str],
        similar_architectures: List[Any]
    ) -> Dict[str, Any]:
        """
        Produce a finalized logical summary applying the tech stack and integrating the architectural
        structures prior to being parsed into the formalized Pydantic `Architecture` module generator.
        """
        # This function acts as a prep-step before architecture_generator
        sys_prompt = "You are a master systems architect. Output a JSON object mapping the exact technical components to be implemented based on the rules and finalized stack."
        user_prompt = f"Stack: {json.dumps(refined_tech_stack)}. Context: {spec.constraints}."
        
        model = await self.model_selector.select_model(ModelComplexity.LOW) # Fast summation
        
        try:
            res_json = await call_llm(sys_prompt, user_prompt, model=model, max_tokens=1000, response_format={"type": "json_object"})
            data = json.loads(res_json)
            
            await self.tracker.track_usage(self.project_id, model, len(user_prompt)//4, len(res_json)//4, "fast")
            
            return {
                "final_tech_stack": refined_tech_stack,
                "adrs": [{"decision_type": d.affected_component, "context": d.decision_context} for d in risky_decisions],
                "design_notes": data
            }
            
        except Exception as e:
            logger.error("hybrid_reasoner_merge_failed", error=str(e))
            return {
                "final_tech_stack": refined_tech_stack,
                "adrs": [],
                "design_notes": {}
            }
