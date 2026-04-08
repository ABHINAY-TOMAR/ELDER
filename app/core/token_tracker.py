from datetime import datetime
from app.core.config import settings

class TokenTracker:
    """ Extracted from RTK Patterns: Manages real-time cost analysis & routing """
    
    # Generic approx pricing per 1K tokens
    PRICING = {
        "claude-haiku": {"input": 0.00025, "output": 0.00125},
        "claude-sonnet-4": {"input": 0.003, "output": 0.015},
        "gpt-4o": {"input": 0.005, "output": 0.015},
        "openrouter-llama3": {"input": 0.0001, "output": 0.0001}
    }

    @staticmethod
    def calculate_cost(model: str, input_tokens: int, output_tokens: int) -> float:
        pricing = TokenTracker.PRICING.get(model, {"input": 0.0, "output": 0.0})
        cost = (input_tokens / 1000.0) * pricing["input"] + (output_tokens / 1000.0) * pricing["output"]
        return cost

    async def track_call(self, project_id: str, reasoning_type: str, model: str, input_tokens: int, output_tokens: int):
        cost = self.calculate_cost(model, input_tokens, output_tokens)
        print(f"[{datetime.now()}] TRACK: {project_id} | {model} | {input_tokens} in / {output_tokens} out | ${cost:.5f}")
        
        # MVP: Mock saving to Supabase
        if settings.SUPABASE_URL:
            # Here we would do a real database.table("token_usage").insert(...)
            pass
            
        return cost

token_tracker = TokenTracker()
