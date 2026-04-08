import os
import structlog
from typing import List, Dict, Optional
from pydantic import BaseModel
from app.models.schemas import RequirementSpec
from app.core.memory import ArchitectMemory

logger = structlog.get_logger("architect_agent.pattern_retriever")

class SimilarArchitecture(BaseModel):
    project_id: str
    similarity_score: float
    tech_stack: Dict[str, str]
    services: List[str]
    lessons_learned: str
    anti_patterns_avoided: List[str]

async def retrieve_similar(spec: RequirementSpec) -> List[SimilarArchitecture]:
    logger.info("retrieving_similar_architectures_start")
    
    memory = ArchitectMemory()
    
    # Text representation of requirements for semantic search
    spec_text = f"Architecture for Features: {', '.join(spec.key_features)}. Constraints: {', '.join(spec.constraints)}. Team Size: {spec.team_size}. Budget: {spec.budget_usd}."
    
    try:
        # Search in the 'architecture' category
        results = await memory.search(
            query=spec_text,
            category="architecture",
            limit=5
        )
        
        matches = []
        for item in results:
            value = item.get("value", {})
            matches.append(SimilarArchitecture(
                project_id=item.get("key", "unknown"),
                similarity_score=item.get("similarity", 0.0), # Assuming rpc returns similarity
                tech_stack=value.get("tech_stack", {}),
                services=value.get("services", []),
                lessons_learned=value.get("lessons_learned", "No specific lessons recorded."),
                anti_patterns_avoided=value.get("anti_patterns_avoided", [])
            ))
            
        logger.info("retrieving_similar_architectures_success", matches=len(matches))
        return matches
        
    except Exception as e:
        logger.error("retrieving_similar_architectures_failed", error=str(e))
        return []
