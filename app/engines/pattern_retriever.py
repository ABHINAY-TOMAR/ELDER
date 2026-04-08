import logging
from typing import List, Dict, Any, Optional
from pydantic import BaseModel, Field
from app.models.requirement_spec import RequirementSpec
from app.core.memory import ArchitectMemory

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class SimilarArchitecture(BaseModel):
    project_id: str
    similarity_score: float
    tech_stack: Dict[str, str]
    services: List[str]
    rationale: str

class PatternRetriever:
    """
    Retrieves similar past architectures using vector search to inform the current design.
    """

    def __init__(self, memory: ArchitectMemory):
        self.memory = memory

    async def retrieve_similar(self, spec: RequirementSpec, limit: int = 5) -> List[SimilarArchitecture]:
        """
        Search pgvector for architectures similar to the current requirement.
        """
        # 1. Create a query string from the spec for embedding
        query_text = (
            f"Project: {spec.project_name}. "
            f"Domain: {spec.domain}. "
            f"Scale: {spec.expected_users} users. "
            f"Features: {', '.join(spec.extracted_features)}. "
            f"Constraints: {', '.join(spec.constraints)}."
        )

        logger.info(f"Retrieving patterns similar to: {spec.project_name}")

        # 2. Search memory (uses Supabase match_architect_memory RPC)
        results = await self.memory.search(
            query=query_text,
            category="architecture",
            limit=limit
        )

        # 3. Format results
        similar = []
        for res in results:
            # result might have 'similarity' key from RPC
            similarity = res.get("similarity", 0.0)
            
            # The 'metadata' field in memory contains the original architecture fields
            metadata = res.get("metadata", {})
            
            similar.append(SimilarArchitecture(
                project_id=res.get("source", "unknown"),
                similarity_score=similarity,
                tech_stack=metadata.get("tech_stack", {}),
                services=metadata.get("services", []),
                rationale=metadata.get("rationale", "No rationale provided.")
            ))

        return similar
