import json
import structlog
from typing import Dict, List
from app.models.schemas import Architecture, FailureMode
from app.engines.llm_client import call_llm

logger = structlog.get_logger("architect_agent.failure_mode_mapper")

SYSTEM_PROMPT = """
You are a Site Reliability Engineer. Identify top 3 failure modes for the given service.
Return output in strictly valid JSON:
{
  "failure_modes": [
    {
      "mode": "...",
      "probability": "high|medium|low",
      "impact": "...",
      "detection_strategy": "...",
      "mitigation_strategy": "...",
      "fallback_strategy": "...",
      "owner": "...",
      "severity": "critical|high|medium|low"
    }
  ]
}
"""

async def map_failure_modes(architecture: Architecture) -> Dict[str, List[FailureMode]]:
    logger.info("mapping_failure_modes_start", services=len(architecture.services))
    
    modes_by_service: Dict[str, List[FailureMode]] = {}
    
    for service in architecture.services:
        prompt = f"""
        Service ID: {service.id}
        Service Name: {service.name}
        Description: {service.description}
        Dependencies: {service.dependencies}
        Tech Stack: {json.dumps(architecture.tech_stack)}
        Domain: {architecture.domain}
        """
        
        try:
            raw_res = await call_llm(
                system_prompt=SYSTEM_PROMPT,
                user_prompt=prompt,
                response_format={"type": "json_object"}
            )
            data = json.loads(raw_res)
            
            fm_list = []
            for fm_data in data.get("failure_modes", []):
                # Ensure literal types are valid
                prob = fm_data.get("probability", "medium").lower()
                sev = fm_data.get("severity", "medium").lower()
                if prob not in ["high", "medium", "low"]: prob = "medium"
                if sev not in ["critical", "high", "medium", "low"]: sev = "medium"
                
                fm_data["probability"] = prob
                fm_data["severity"] = sev
                
                try:
                    fm = FailureMode(**fm_data)
                    fm_list.append(fm)
                except Exception as ex:
                    logger.warning("invalid_failure_mode_dropped", error=str(ex), data=fm_data)
                    
            modes_by_service[service.id] = fm_list
            logger.debug("failure_modes_mapped_for_service", service=service.id, count=len(fm_list))
            
        except Exception as e:
            logger.error("failure_mode_mapping_failed", error=str(e), service=service.id)
            modes_by_service[service.id] = []
            
    logger.info("mapping_failure_modes_complete")
    return modes_by_service
