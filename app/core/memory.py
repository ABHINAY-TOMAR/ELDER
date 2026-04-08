import logging
from supabase import create_client, Client
from app.core.config import settings

logger = logging.getLogger(__name__)


def get_supabase_client() -> Client | None:
    """Create and return a Supabase client. Returns None if not configured."""
    if not settings.SUPABASE_URL or not settings.SUPABASE_KEY:
        logger.warning("Supabase URL or Key not configured. Memory features disabled.")
        return None
    try:
        return create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
    except Exception as e:
        logger.error(f"Failed to create Supabase client: {e}")
        return None


class ArchitectureMemory:
    """Production-ready memory interface backed by Supabase pgvector."""

    def __init__(self):
        self.db = get_supabase_client()

    def _is_ready(self) -> bool:
        return self.db is not None

    async def store_architecture(
        self, project_id: str, architecture_json: dict, embedding: list[float]
    ) -> bool:
        """Store a proposed architecture with its corresponding pgvector embedding."""
        if not self._is_ready():
            logger.info("Supabase not configured — skipping architecture storage.")
            return False
        try:
            self.db.table("architecture_embeddings").insert(
                {
                    "project_id": project_id,
                    "architecture": architecture_json,
                    "embedding": embedding,
                }
            ).execute()
            logger.info(f"Stored architecture for project {project_id}")
            return True
        except Exception as e:
            logger.error(f"Failed to store architecture: {e}")
            return False

    async def find_similar_architectures(
        self, query_embedding: list[float], limit: int = 5
    ) -> list[dict]:
        """Semantic search for similar past designs using pgvector RPC."""
        if not self._is_ready():
            return []
        try:
            result = self.db.rpc(
                "match_architectures",
                {
                    "query_embedding": query_embedding,
                    "match_count": limit,
                },
            ).execute()
            return result.data if result.data else []
        except Exception as e:
            logger.warning(f"Semantic search unavailable (RPC may not exist yet): {e}")
            return []

    async def track_token_usage(
        self,
        project_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        cost_usd: float,
        reasoning_type: str = "fast",
    ) -> bool:
        """Record token usage to the token_usage table."""
        if not self._is_ready():
            return False
        try:
            self.db.table("token_usage").insert(
                {
                    "project_id": project_id,
                    "model": model,
                    "input_tokens": input_tokens,
                    "output_tokens": output_tokens,
                    "cost_usd": cost_usd,
                    "reasoning_type": reasoning_type,
                }
            ).execute()
            return True
        except Exception as e:
            logger.error(f"Failed to track token usage: {e}")
            return False


architecture_memory = ArchitectureMemory()
