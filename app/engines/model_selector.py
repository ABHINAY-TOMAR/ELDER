from typing import Literal, Optional, Dict
from enum import Enum

class ModelComplexity(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"

class ModelSelector:
    """
    Selects reasoning model based on task type, complexity, and available budget.
    Drawn from FastCode patterns.
    """
    
    MODELS = {
        "claude-3-5-haiku-20241022": {
            "speed": 0.95,
            "cost": 0.25, # input/output combined weight
            "quality": 0.70,
            "max_tokens": 4096
        },
        "claude-3-5-sonnet-20241022": {
            "speed": 0.60,
            "cost": 3.00,
            "quality": 0.95,
            "max_tokens": 8192
        }
    }

    async def select_model(
        self,
        complexity: ModelComplexity,
        budget_remaining: Optional[float] = None,
        use_extended_thinking: bool = False
    ) -> str:
        """Determines best model for a reasoning task."""
        
        # High complexity or explicit deep thinking request always forces Sonnet
        if complexity == ModelComplexity.HIGH or use_extended_thinking:
            return "anthropic/claude-3-5-sonnet-20241022" if os.getenv("OPENROUTER_API_KEY") else "claude-3-5-sonnet-20241022"
            
        # If budget is extremely constrained, fallback to Haiku regardless of medium complexity
        if budget_remaining and budget_remaining < 0.05:
             return "claude-3-5-haiku-20241022"
             
        # Medium complexity: Sonnet if budget allows, else Haiku
        if complexity == ModelComplexity.MEDIUM:
            if budget_remaining and budget_remaining > 0.5:
                return "claude-3-5-sonnet-20241022"
            else:
                return "claude-3-5-haiku-20241022"
        
        # Low complexity: Always Haiku
        return "claude-3-5-haiku-20241022"

import os
