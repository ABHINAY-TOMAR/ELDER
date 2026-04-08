import os
import json
import logging
import asyncio
from typing import Dict, Any, Optional, List, Union
import httpx
from pydantic import ValidationError

from app.models.requirement_spec import RequirementSpec
from app.core.token_tracker import ArchitectTokenTracker

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class RequirementParser:
    """
    Engine to parse natural language requirements into a structured RequirementSpec.
    Uses OpenAI (GPT-4o-mini) for fast, cost-effective extraction.
    """

    SYSTEM_PROMPT = """
    You are an expert software architect. Your task is to extract structured requirements from a natural language description.
    
    Extract the following fields in JSON format:
    - project_name: string
    - domain: "microservices", "ai_native", "data_pipeline", or "hybrid"
    - team_size: integer (default 2 if not mentioned)
    - budget_usd: integer (default 5000 if not mentioned)
    - expected_users: integer (default 1000 if not mentioned)
    - latency_requirement_ms: integer (default 500 if not mentioned)
    - data_sensitivity: "public", "internal", "pii", or "regulated"
    - deployment_target: "cloud", "on_prem", "hybrid", or "edge"
    - constraints: list of strings
    - timeline_weeks: integer (default 4 if not mentioned)
    - extracted_features: list of strings (core functional requirements)

    If a value is not explicitly mentioned, provide a reasonable estimate based on the context or use the default.
    Return ONLY the raw JSON object.
    """

    def __init__(self, token_tracker: Optional[ArchitectTokenTracker] = None):
        self.api_key = os.getenv("OPENAI_API_KEY")
        self.model = "gpt-4o-mini"
        self.token_tracker = token_tracker

    async def parse(self, text: str) -> RequirementSpec:
        """
        Parse raw text into a RequirementSpec object.
        """
        if not self.api_key:
            logger.warning("OPENAI_API_KEY not found. Returning default RequirementSpec.")
            return RequirementSpec(project_name="Untitled Project")

        if not text or len(text.strip()) < 10:
            logger.error("Input text too short for parsing.")
            raise ValueError("Input text is too short to be a valid requirement.")

        logger.info(f"Parsing requirements (len={len(text)})...")

        payload = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": self.SYSTEM_PROMPT},
                {"role": "user", "content": f"Extract requirements from this text:\n\n{text}"}
            ],
            "response_format": {"type": "json_object"},
            "temperature": 0.1
        }

        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    "https://api.openai.com/v1/chat/completions",
                    headers={
                        "Authorization": f"Bearer {self.api_key}",
                        "Content-Type": "application/json"
                    },
                    json=payload,
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()
                
                # Track tokens if tracker is provided
                if self.token_tracker:
                    usage = result.get("usage", {})
                    await self.token_tracker.track_usage(
                        project_id="internal_parsing", # Or pass from caller
                        model=self.model,
                        input_tokens=usage.get("prompt_tokens", 0),
                        output_tokens=usage.get("completion_tokens", 0),
                        reasoning_type="fast"
                    )

                content = result["choices"][0]["message"]["content"]
                parsed_data = json.loads(content)
                
                # Create Pydantic model
                spec = RequirementSpec(**parsed_data)
                return spec

            except httpx.HTTPStatusError as e:
                logger.error(f"HTTP error during parsing: {e.response.text}")
                raise RuntimeError(f"OpenAI API error: {e.response.status_code}")
            except (json.JSONDecodeError, KeyError, ValidationError) as e:
                logger.error(f"Failed to parse OpenAI response: {e}")
                raise RuntimeError(f"Parsing engine failed to produce valid schema: {str(e)}")
            except Exception as e:
                logger.error(f"Unexpected error during parsing: {e}")
                raise
