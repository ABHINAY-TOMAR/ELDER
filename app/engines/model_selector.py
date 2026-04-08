import logging
from typing import Literal, Optional, List
from pydantic import BaseModel

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ModelSelector:
    """
    Intelligent model selector that chooses the optimal LLM based on task complexity and budget.
    """

    def __init__(self, default_model: str = "claude-3-5-sonnet"):
        self.default_model = default_model

    def select(
        self, 
        complexity: Literal["low", "medium", "high"], 
        budget_remaining_usd: float,
        is_risky: bool = False
    ) -> str:
        """
        Choose between fast/cheap models (Haiku) and deep/expensive models (Sonnet/o1).
        """
        # 1. High-risk or high-complexity always gets the best model if budget allows
        if (complexity == "high" or is_risky) and budget_remaining_usd > 5.0:
            logger.info("Selecting high-performance model (Sonnet) due to complexity/risk.")
            return "claude-3-5-sonnet"
        
        # 2. Medium complexity with decent budget
        if complexity == "medium" and budget_remaining_usd > 2.0:
            return "claude-3-5-sonnet"
        
        # 3. Budget constrained or low complexity
        if budget_remaining_usd < 0.50:
            logger.warning("Budget extremely low. Forcing low-cost model (Haiku).")
            return "claude-3-5-haiku"
            
        if complexity == "low":
            return "claude-3-5-haiku"

        # Default fallback
        return self.default_model

    def get_reasoning_config(self, model: str) -> dict:
        """Return model-specific inference parameters."""
        if "sonnet" in model:
            return {"temperature": 0.5, "max_tokens": 4000}
        elif "haiku" in model:
            return {"temperature": 0.2, "max_tokens": 2000}
        elif "o1" in model:
            return {"temperature": 1.0, "max_tokens": 8000}
        return {"temperature": 0.7, "max_tokens": 2000}
