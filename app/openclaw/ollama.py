"""Ollama API client for OpenClaw Bridge Server."""

import httpx
from .config import OLLAMA_BASE_URL

TIMEOUT = 120.0  # seconds


async def check_health() -> dict:
    """Check Ollama API availability and list models."""
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            resp = await client.get(f"{OLLAMA_BASE_URL}/api/tags")
            resp.raise_for_status()
            data = resp.json()
            model_names = [m["name"] for m in data.get("models", [])]
            return {"ok": True, "models": model_names}
    except Exception as e:
        return {"ok": False, "error": str(e), "models": []}


async def check_model_available(model_name: str) -> bool:
    """Check if a specific model is available in Ollama."""
    result = await check_health()
    if not result["ok"]:
        return False
    return model_name in result["models"]


async def chat(
    model: str,
    messages: list[dict],
    temperature: float = 0.3,
    stream: bool = False,
    keep_alive: int | str = -1,  # Keep loaded indefinitely by default
) -> dict:
    """Send a chat request to Ollama.

    Args:
        model: Model name (e.g., "gemma3:4b").
        messages: List of message dicts with "role" and "content".
        temperature: Sampling temperature.
        stream: Whether to stream (not used in MVP).

    Returns:
        dict with "ok", "content", and "model".
    """
    try:
        async with httpx.AsyncClient(timeout=TIMEOUT) as client:
            payload = {
                "model": model,
                "messages": messages,
                "stream": False,
                "keep_alive": keep_alive,
                "options": {
                    "temperature": temperature,
                    "num_ctx": 16384,     # 16K context window to support large source files and instructions
                    "num_predict": 4096,  # 4K output generation limit to guarantee full file printing without cuts
                },
            }
            resp = await client.post(
                f"{OLLAMA_BASE_URL}/api/chat",
                json=payload,
            )
            resp.raise_for_status()
            data = resp.json()
            content = data.get("message", {}).get("content", "")
            return {
                "ok": True,
                "content": content,
                "model": model,
                "total_duration": data.get("total_duration"),
                "eval_count": data.get("eval_count"),
            }
    except httpx.TimeoutException:
        return {"ok": False, "content": "", "model": model, "error": "Ollama request timed out"}
    except Exception as e:
        return {"ok": False, "content": "", "model": model, "error": str(e)}
