import json
import structlog
import uuid
from typing import Dict, Any, List, Literal

from app.models.schemas import RequirementSpec, Architecture, Service, DataFlow, ADR
from app.engines.llm_client import call_llm

logger = structlog.get_logger("architect_agent.architecture_generator")

SYSTEM_PROMPT = """
You are an expert Systems Architect. You are given a project spec, a domain, and a finalized tech stack.
Return a full architectural decomposition in JSON format exactly matching the schema.
Schema:
{
  "services": [{"id": "...", "name": "...", "description": "...", "dependencies": ["..."]}],
  "data_flows": [{"producer": "...", "consumer": "...", "sync_type": "...", "format": "..."}],
  "adrs": [{"title": "...", "context": "...", "decision": "...", "rationale": "..."}],
  "estimated_effort_weeks": <int>
}
"""

async def generate(spec: RequirementSpec, domain: Literal["microservices", "ai_native", "data_pipeline"], tech_stack: Dict[str, str]) -> Architecture:
    """
    Decomposes the final architecture intelligently using LLM into explicit models.
    """
    logger.info("generating_architecture_start", domain=domain)
    
    prompt = f"""
    Project Features: {spec.key_features}
    Constraints: {spec.constraints}
    Domain: {domain}
    Tech Stack: {json.dumps(tech_stack)}
    
    Break this down into explicit microservices/components. Do not introduce circular dependencies.
    """
    
    try:
        raw_response = await call_llm(
            system_prompt=SYSTEM_PROMPT,
            user_prompt=prompt,
            response_format={"type": "json_object"},
            max_tokens=4000
        )
        data = json.loads(raw_response)
        
        services = [Service(**s) for s in data.get("services", [])]
        data_flows = [DataFlow(**df) for df in data.get("data_flows", [])]
        adrs = [ADR(**adr) for adr in data.get("adrs", [])]
        effort = max(1, min(52, data.get("estimated_effort_weeks", 4)))
        
        arch = Architecture(
            project_id=str(uuid.uuid4()),
            project_name="Generated Project",
            domain=domain,
            services=services,
            tech_stack=tech_stack,
            adrs=adrs,
            failure_modes={},
            data_flows=data_flows,
            implementation_phases=[],
            estimated_effort_weeks=effort
        )
        
        logger.info("generating_architecture_success", services_count=len(services))
        return arch
        
    except Exception as e:
        logger.error("architecture_generation_failed", error=str(e))
        # Fallback empty architecture
        return Architecture(
            project_id=str(uuid.uuid4()),
            project_name="Error Generating Project",
            domain=domain,
            services=[], tech_stack=tech_stack, adrs=[], failure_modes={}, data_flows=[], implementation_phases=[], estimated_effort_weeks=4
        )
