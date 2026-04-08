import logging
import json
import os
import httpx
from typing import List, Dict, Any, Optional
from app.models.requirement_spec import RequirementSpec
from app.models.architecture import Architecture, Service, ADR, FailureMode
from app.engines.hybrid_reasoner import FinalArchitectureRecommendation

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArchitectureGenerator:
    """
    Decomposes an architecture recommendation into detailed services, ADRs, and effort estimates.
    """

    def __init__(self):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o"

    async def generate(
        self, 
        project_id: str,
        spec: RequirementSpec, 
        recommendation: FinalArchitectureRecommendation
    ) -> Architecture:
        """
        Produce a full Architecture object from requirements and reasoning.
        """
        logger.info(f"Generating full architecture for {spec.project_name}...")

        # 1. Decompose into Services
        services = await self._decompose_services(spec, recommendation)
        
        # 2. Generate ADRs (based on deep reasoning + standard patterns)
        adrs = self._generate_adrs(spec, recommendation)
        
        # 3. Estimate Effort
        effort = self._estimate_effort(services, spec.team_size)

        return Architecture(
            project_id=project_id,
            project_name=spec.project_name,
            domain=spec.domain,
            tech_stack=recommendation.tech_stack,
            services=services,
            adrs=adrs,
            estimated_effort_weeks=effort,
            rationale=recommendation.rationale
        )

    async def _decompose_services(
        self, 
        spec: RequirementSpec, 
        recommendation: FinalArchitectureRecommendation
    ) -> List[Service]:
        """
        Use LLM to identify the specific services needed for the architecture.
        """
        if not self.api_key:
            # Simple fallback for local dev
            return [
                Service(
                    id="api-gateway", 
                    name="API Gateway", 
                    description="Main entry point", 
                    stack=recommendation.tech_stack.get("api_framework", "FastAPI")
                ),
                Service(
                    id="core-service", 
                    name="Core Business Logic", 
                    description="Handles main features", 
                    stack=recommendation.tech_stack.get("api_framework", "FastAPI"),
                    dependencies=["api-gateway"]
                )
            ]

        prompt = f"""
        Requirements: {spec.model_dump_json()}
        Tech Stack: {json.dumps(recommendation.tech_stack)}
        Domain: {spec.domain}
        
        Decompose this system into a logical set of microservices or components.
        For each service, provide:
        - id (slug)
        - name
        - description
        - specific stack from the provided tech stack
        - dependencies (list of service ids it depends on)
        - main endpoints (list of strings)
        
        Return a JSON list of services.
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
                        "temperature": 0.3
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                data = response.json()
                content = json.loads(data["choices"][0]["message"]["content"])
                
                # The LLM might return {"services": [...]}
                services_raw = content.get("services", content)
                return [Service(**s) for s in services_raw]
            except Exception as e:
                logger.error(f"Service decomposition failed: {e}")
                return []

    def _generate_adrs(
        self, 
        spec: RequirementSpec, 
        recommendation: FinalArchitectureRecommendation
    ) -> List[ADR]:
        """
        Generate Architecture Decision Records based on the chosen stack and reasoning.
        """
        adrs = []
        
        # 1. Main database decision
        db = recommendation.tech_stack.get("database", "PostgreSQL")
        adrs.append(ADR(
            title=f"Choice of {db} as primary database",
            context=f"Project needs to handle {spec.expected_users} users with {spec.data_sensitivity} sensitivity.",
            decision=f"Use {db}.",
            alternatives=["MongoDB", "DynamoDB"],
            consequences="Ensures data integrity and matches team skills."
        ))

        # 2. Add ADRs from deep reasoning
        for thought in recommendation.deep_reasoning_applied:
            adrs.append(ADR(
                title=f"Decision: {thought.decision_type}",
                context=thought.reasoning,
                decision=thought.refined_recommendation,
                alternatives=[thought.original_recommendation],
                consequences=thought.risk_mitigation
            ))
            
        return adrs

    def _estimate_effort(self, services: List[Service], team_size: int) -> int:
        """
        Rough heuristic for development effort in weeks.
        """
        base_weeks_per_service = 1.5
        complexity_factor = 1.2
        total_work = len(services) * base_weeks_per_service * complexity_factor
        
        # Diminishing returns on team size (Brooks' Law)
        effective_team_size = team_size ** 0.8
        
        estimated = round(total_work / effective_team_size)
        return max(2, estimated)
