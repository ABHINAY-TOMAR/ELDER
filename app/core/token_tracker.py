import os
import json
import logging
import math
from datetime import datetime, timedelta
from typing import Dict, Any, Optional, List, Union
from supabase import create_client, Client

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ArchitectTokenTracker:
    """
    Advanced token tracking and cost management system for the Architect Agent.
    
    This system records all LLM interactions, calculates real-time costs based on 
    current model pricing, and provides aggregated statistics for project management 
    and budget tracking.
    
    Attributes:
        PRICING (Dict): Real-time pricing data for various LLM models (USD per 1M tokens).
        RETENTION_DAYS (int): How long to keep tracking data before cleanup.
    """
    
    # Pricing per 1,000,000 tokens (USD)
    # Updated as of April 2026 based on standard provider rates
    PRICING = {
        "claude-3-5-sonnet": {
            "input": 3.0,
            "output": 15.0,
            "display_name": "Anthropic Claude 3.5 Sonnet"
        },
        "claude-3-5-haiku": {
            "input": 0.25,
            "output": 1.25,
            "display_name": "Anthropic Claude 3.5 Haiku"
        },
        "claude-3-opus": {
            "input": 15.0,
            "output": 75.0,
            "display_name": "Anthropic Claude 3 Opus"
        },
        "gpt-4o": {
            "input": 5.0,
            "output": 15.0,
            "display_name": "OpenAI GPT-4o"
        },
        "gpt-4o-mini": {
            "input": 0.15,
            "output": 0.60,
            "display_name": "OpenAI GPT-4o Mini"
        },
        "o1-preview": {
            "input": 15.0,
            "output": 60.0,
            "display_name": "OpenAI o1-preview"
        },
        "o1-mini": {
            "input": 3.0,
            "output": 12.0,
            "display_name": "OpenAI o1-mini"
        },
        "deepseek-chat": {
            "input": 0.07,
            "output": 1.10,
            "display_name": "DeepSeek Chat (V3)"
        },
        "gemini-1.5-pro": {
            "input": 3.5,
            "output": 10.5,
            "display_name": "Google Gemini 1.5 Pro"
        },
        "gemini-1.5-flash": {
            "input": 0.075,
            "output": 0.30,
            "display_name": "Google Gemini 1.5 Flash"
        }
    }

    RETENTION_DAYS = 90  # Keep history for 90 days

    def __init__(self):
        """Initialize the tracker with Supabase client connection."""
        self.supabase_url = os.getenv("SUPABASE_URL")
        self.supabase_key = os.getenv("SUPABASE_KEY")
        
        if self.supabase_url and self.supabase_key:
            try:
                self.client: Client = create_client(self.supabase_url, self.supabase_key)
            except Exception as e:
                logger.error(f"Failed to initialize Supabase client: {e}")
                self.client = None
        else:
            logger.warning("Supabase credentials missing. Usage tracking will be local-only.")
            self.client = None

    @staticmethod
    def estimate_tokens(text: str) -> int:
        """
        Fast heuristic to estimate token count from text.
        Uses the standard rule of thumb: ~4 characters per token.
        
        Args:
            text: The raw string to estimate.
            
        Returns:
            int: Estimated number of tokens.
        """
        if not text:
            return 0
        return math.ceil(len(text) / 4.0)

    def calculate_cost(self, model: str, input_tokens: int, output_tokens: int) -> float:
        """
        Calculate the USD cost for a specific LLM interaction.
        
        Args:
            model: Name/identifier of the model used.
            input_tokens: Number of prompt/input tokens.
            output_tokens: Number of completion/output tokens.
            
        Returns:
            float: Total cost in USD.
        """
        # Find the best matching model in our pricing table
        selected_model = "claude-3-5-sonnet"  # Default fallback
        model_lower = model.lower()
        
        for name in self.PRICING.keys():
            if name in model_lower:
                selected_model = name
                break
        
        pricing = self.PRICING[selected_model]
        input_cost = (input_tokens / 1_000_000.0) * pricing["input"]
        output_cost = (output_tokens / 1_000_000.0) * pricing["output"]
        
        return input_cost + output_cost

    async def track_usage(
        self,
        project_id: str,
        model: str,
        input_tokens: int,
        output_tokens: int,
        reasoning_type: str = "fast",
        metadata: Optional[Dict[str, Any]] = None
    ) -> float:
        """
        Record token usage and cost for a project.
        
        Args:
            project_id: Unique identifier for the current project.
            model: Name of the model used.
            input_tokens: Count of input tokens.
            output_tokens: Count of output tokens.
            reasoning_type: Category of reasoning ("fast", "deep", "structured").
            metadata: Optional additional context for the log entry.
            
        Returns:
            float: The calculated cost in USD.
        """
        cost_usd = self.calculate_cost(model, input_tokens, output_tokens)
        total_tokens = input_tokens + output_tokens
        
        entry = {
            "project_id": project_id,
            "model": model,
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
            "total_tokens": total_tokens,
            "cost_usd": cost_usd,
            "reasoning_type": reasoning_type,
            "metadata": metadata or {},
            "created_at": datetime.now().isoformat()
        }
        
        logger.info(f"Tracking usage for project {project_id}: {total_tokens} tokens (${cost_usd:.6f})")
        
        if self.client:
            try:
                # Insert record into Supabase token_usage table
                self.client.table("token_usage").insert(entry).execute()
            except Exception as e:
                logger.error(f"Failed to push usage data to Supabase: {e}")
        
        return cost_usd

    async def get_project_summary(self, project_id: str) -> Dict[str, Any]:
        """
        Retrieve a detailed cost summary for a specific project.
        
        Args:
            project_id: The project ID to summarize.
            
        Returns:
            Dict: Aggregated metrics including total cost, token breakdown, 
                  and cost by reasoning type.
        """
        if not self.client:
            return {"total_cost": 0.0, "total_tokens": 0, "status": "local_mode"}
            
        try:
            result = self.client.table("token_usage") \
                .select("cost_usd, total_tokens, input_tokens, output_tokens, reasoning_type") \
                .eq("project_id", project_id) \
                .execute()
            
            data = result.data or []
            if not data:
                return {
                    "total_cost": 0.0,
                    "total_tokens": 0,
                    "input_tokens": 0,
                    "output_tokens": 0,
                    "breakdown": {}
                }
            
            summary = {
                "total_cost": sum(d["cost_usd"] for d in data),
                "total_tokens": sum(d["total_tokens"] for d in data),
                "input_tokens": sum(d["input_tokens"] for d in data),
                "output_tokens": sum(d["output_tokens"] for d in data),
                "breakdown": {
                    "fast": sum(d["cost_usd"] for d in data if d["reasoning_type"] == "fast"),
                    "deep": sum(d["cost_usd"] for d in data if d["reasoning_type"] == "deep"),
                    "structured": sum(d["cost_usd"] for d in data if d["reasoning_type"] == "structured"),
                }
            }
            return summary
        except Exception as e:
            logger.error(f"Error fetching project summary: {e}")
            return {"error": str(e)}

    async def get_usage_history(
        self, 
        project_id: Optional[str] = None, 
        days: int = 30
    ) -> List[Dict[str, Any]]:
        """
        Get usage history logs.
        
        Args:
            project_id: Optional filter for a specific project.
            days: Number of days to look back.
            
        Returns:
            List[Dict]: List of usage records.
        """
        if not self.client:
            return []
            
        cutoff = (datetime.now() - timedelta(days=days)).isoformat()
        
        try:
            query = self.client.table("token_usage").select("*").gte("created_at", cutoff)
            if project_id:
                query = query.eq("project_id", project_id)
            
            result = query.order("created_at", desc=True).execute()
            return result.data or []
        except Exception as e:
            logger.error(f"Error fetching usage history: {e}")
            return []

    async def get_daily_stats(self, days: int = 30) -> List[Dict[str, Any]]:
        """
        Get daily aggregated cost and token stats.
        Note: For performance, this usually calls a Supabase RPC function.
        If the RPC is missing, it performs in-memory aggregation.
        
        Args:
            days: History window in days.
            
        Returns:
            List[Dict]: Daily stats with date, total_cost, total_tokens.
        """
        if not self.client:
            return []
            
        try:
            # Attempt to use a database function for efficiency
            # rpc 'get_daily_token_stats' should be defined in Supabase
            result = self.client.rpc("get_daily_token_stats", {"days_limit": days}).execute()
            return result.data or []
        except Exception:
            # Fallback: Manual aggregation
            logger.info("RPC 'get_daily_token_stats' not found. Performing manual aggregation.")
            all_data = await self.get_usage_history(days=days)
            
            daily_agg = {}
            for entry in all_data:
                day = entry["created_at"][:10]  # YYYY-MM-DD
                if day not in daily_agg:
                    daily_agg[day] = {"date": day, "total_cost": 0.0, "total_tokens": 0}
                
                daily_agg[day]["total_cost"] += entry["cost_usd"]
                daily_agg[day]["total_tokens"] += entry["total_tokens"]
                
            # Return sorted by date
            return sorted(daily_agg.values(), key=lambda x: x["date"], reverse=True)

    async def cleanup_old_records(self) -> int:
        """
        Remove tracking records older than RETENTION_DAYS.
        
        Returns:
            int: Number of records deleted.
        """
        if not self.client:
            return 0
            
        cutoff = (datetime.now() - timedelta(days=self.RETENTION_DAYS)).isoformat()
        
        try:
            result = self.client.table("token_usage").delete().lt("created_at", cutoff).execute()
            # result.data usually contains the deleted rows
            count = len(result.data) if result.data else 0
            logger.info(f"Retention cleanup complete: {count} records deleted.")
            return count
        except Exception as e:
            logger.error(f"Failed to cleanup old records: {e}")
            return 0

    def get_model_info(self, model: str) -> Dict[str, Any]:
        """
        Get friendly name and current pricing for a model.
        
        Args:
            model: Model identifier.
            
        Returns:
            Dict: Model metadata.
        """
        model_lower = model.lower()
        for name, info in self.PRICING.items():
            if name in model_lower:
                return {
                    "id": name,
                    "display_name": info["display_name"],
                    "input_price": info["input"],
                    "output_price": info["output"]
                }
        return {
            "id": "unknown",
            "display_name": model,
            "input_price": 0.0,
            "output_price": 0.0
        }

    async def get_budget_alert(self, project_id: str, limit_usd: float) -> Dict[str, Any]:
        """
        Check if a project has exceeded or is near a budget limit.
        
        Args:
            project_id: Project to check.
            limit_usd: Budget limit in USD.
            
        Returns:
            Dict: Alert status and percentage used.
        """
        summary = await self.get_project_summary(project_id)
        total_cost = summary.get("total_cost", 0.0)
        percent = (total_cost / limit_usd) * 100 if limit_usd > 0 else 0
        
        return {
            "project_id": project_id,
            "budget_limit": limit_usd,
            "current_spend": total_cost,
            "percent_used": percent,
            "is_exceeded": total_cost > limit_usd,
            "is_near_limit": percent > 80.0
        }
