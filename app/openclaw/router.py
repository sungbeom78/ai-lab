"""Intent router: determines which Ollama model to use based on message content."""

from .config import CHAT_MODEL, CODE_MODEL
from . import ollama

async def classify_intent(message: str, mode: str = "auto") -> dict:
    """Classify user intent and select appropriate model using LLM.

    Args:
        message: User's message text.
        mode: "auto", "chat", or "code". Can be comma-separated multiple modes.

    Returns:
        dict with 'route' ("chat" or "code") and 'model' name.
    """
    # 쉼표로 구분된 다중 모드 리스트 분석
    modes = [m.strip().lower() for m in mode.split(',')] if mode else []

    # [CRITICAL HOTFIX] 다중 모드 중 develop(개발) 또는 validate(검증)이 단 하나라도 포함되어 있다면,
    # 사용자의 명시적인 코드 수정 목적이 확인된 것이므로, 챗 분류기를 태우지 않고
    # 무조건 고성능 코딩 모델인 CODE_MODEL (qwen)로 직행 라우팅한다!
    if "develop" in modes or "validate" in modes or mode == "code":
        return {"route": "code", "model": CODE_MODEL, "reason": f"develop/validate/code mode active (forced code model: {CODE_MODEL})"}

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
