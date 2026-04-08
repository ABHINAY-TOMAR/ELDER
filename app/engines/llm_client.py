import os
import httpx
from typing import Optional, Dict

async def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: Optional[str] = None,
    temperature: float = 0.0,
    max_tokens: int = 1000,
    response_format: Optional[Dict] = None
) -> str:
    """
    Generic LLM client that supports OpenAI-compatible APIs (OpenAI, OpenRouter, DeepSeek, NVIDIA, Kimi/Moonshot, etc.).
    Defaults to OpenRouter if OPENROUTER_API_KEY is set, else leverages generic LLM_BASE_URL.
    """
    # Key selection priority
    api_key = (
        os.getenv("OPENROUTER_API_KEY") or 
        os.getenv("OPENAI_API_KEY") or 
        os.getenv("DEEPSEEK_API_KEY") or 
        os.getenv("NVIDIA_API_KEY") or
        os.getenv("KIMI_API_KEY") or
        os.getenv("LLM_API_KEY")
    )
    
    # URL selection priority
    if os.getenv("OPENROUTER_API_KEY"):
        base_url = "https://openrouter.ai/api/v1"
        default_model = "openai/gpt-4o-mini"
    elif os.getenv("DEEPSEEK_API_KEY"):
        base_url = "https://api.deepseek.com/v1"
        default_model = "deepseek-chat"
    elif os.getenv("OPENAI_API_KEY"):
        base_url = "https://api.openai.com/v1"
        default_model = "gpt-3.5-turbo"
    else:
        # Fallback to custom config if standard ones aren't set
        base_url = os.getenv("LLM_BASE_URL", "https://api.openai.com/v1")
        default_model = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

    # The user can override model in the function call, otherwise fallback to the calculated default or env
    model_name = model or os.getenv("LLM_MODEL", default_model)

    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }

    # OpenRouter specific headers (optional but recommended for routing)
    if "openrouter" in base_url:
        headers["HTTP-Referer"] = "http://localhost:8000"
        headers["X-Title"] = "Architect Agent AI"

    payload = {
        "model": model_name,
        "messages": [
            {"role": "system", "content": system_prompt},
            {"role": "user", "content": user_prompt}
        ],
        "temperature": temperature,
        "max_tokens": max_tokens
    }

    if response_format:
        payload["response_format"] = response_format

    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(f"{base_url}/chat/completions", headers=headers, json=payload, timeout=60.0)
            response.raise_for_status()
            data = response.json()
            
            if "error" in data:
                raise LLMError(f"API error: {data['error']}")
            
            if not data.get("choices") or not data["choices"][0].get("message"):
                raise LLMError("Invalid response format from LLM API")
            
            return data["choices"][0]["message"]["content"]
            
        except httpx.TimeoutException:
            raise LLMError(f"Request timed out after 60 seconds to {base_url}")
        except httpx.HTTPStatusError as e:
            raise LLMError(f"HTTP error {e.response.status_code}: {e.response.text[:200]}")
        except httpx.RequestError as e:
            raise LLMError(f"Request failed: {str(e)}")
        except (KeyError, IndexError, ValueError) as e:
            raise LLMError(f"Invalid response parsing: {str(e)}")


class LLMError(Exception):
    """Custom exception for LLM API errors."""
    pass
