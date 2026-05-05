"""Intent router: determines which Ollama model to use based on message content."""

from .config import CHAT_MODEL, CODE_MODEL
from . import ollama

async def classify_intent(message: str, mode: str = "auto") -> dict:
    """Classify user intent and select appropriate model using LLM.

    Args:
        message: User's message text.
        mode: "auto", "chat", or "code". If not auto, forces the mode.

    Returns:
        dict with 'route' ("chat" or "code") and 'model' name.
    """
    if mode == "code":
        return {"route": "code", "model": CODE_MODEL, "reason": "mode=code (forced)"}

    if mode == "chat":
        return {"route": "chat", "model": CHAT_MODEL, "reason": "mode=chat (forced)"}

    # Auto mode: Use Gemma to classify
    lines = [line for line in message.splitlines() if line.strip()]
    if len(lines) <= 6:
        context_text = "\n".join(lines)
    else:
        context_text = "\n".join(lines[:3]) + "\n...\n" + "\n".join(lines[-3:])

    system_prompt = (
        "다음 사용자의 메시지 문맥(앞 3줄, 뒤 3줄)을 보고, "
        "이 메시지가 '코드 작성, 수정, 에러 분석, 프로젝트 구조 변경 등 프로그래밍 작업'에 대한 요청인지 판단하라. "
        "만약 코드/작업에 대한 수정 요청이면 대문자로 'YES', 일상적인 대화나 단순 인사면 'NO' 라고만 출력하라."
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": context_text},
    ]

    result = await ollama.chat(
        model=CHAT_MODEL,
        messages=messages,
        temperature=0.1,  # Low temp for deterministic routing
        keep_alive=-1,
    )

    if not result.get("ok"):
        return {"route": "chat", "model": CHAT_MODEL, "reason": f"fallback due to err: {result.get('error')}"}

    answer = result.get("content", "").strip().upper()

    if "YES" in answer:
        return {"route": "code", "model": CODE_MODEL, "reason": "LLM classified as CODE"}
    else:
        return {"route": "chat", "model": CHAT_MODEL, "reason": "LLM classified as CHAT"}
