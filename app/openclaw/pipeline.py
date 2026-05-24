"""3-Stage Evaluation Pipeline for OpenClaw.

Evaluates structure -> development steps -> final instruction.
"""

import app.openclaw.ollama as ollama


async def run_3_stage_pipeline(user_request: str, workspace_context: str, base_model: str = "gemma3:4b") -> str:
    """Run a 3-stage evaluation and return a final consolidated instruction.
    
    Args:
        user_request: The user's original message or instruction content.
        workspace_context: The workspace tree and active file context.
        base_model: The fast model to use for the evaluation stages.
        
    Returns:
        The final stage 3 output string.
    """
    
    print("[Pipeline] Starting Stage 1: Structural Analysis")
    stage1_prompt = (
        f"당신은 시스템 아키텍트입니다. 다음 문맥을 기반으로 사용자의 요청에 대한 구조적 타당성과 범위를 분석하세요.\n"
        f"반드시 한국어로 작성하세요.\n\n"
        f"## Workspace Context:\n{workspace_context}\n\n"
        f"## User Request:\n{user_request}\n\n"
        f"분석 내용 (현재 구조, 필요한 모듈, 위험 요소 등):"
    )
    res1 = await ollama.chat(model=base_model, messages=[{"role": "user", "content": stage1_prompt}], temperature=0.2)
    stage1_out = res1.get("answer", "Stage 1 Failed")

    print("[Pipeline] Starting Stage 2: Practical Development Analysis")
    stage2_prompt = (
        f"당신은 시니어 개발자입니다. 아키텍트의 분석을 바탕으로 구체적인 기술 스택, 수정할 파일 경로, 예상되는 문제점과 구현 단계를 도출하세요.\n"
        f"반드시 한국어로 작성하세요.\n\n"
        f"## Architect Analysis (Stage 1):\n{stage1_out}\n\n"
        f"## Original Request:\n{user_request}\n\n"
        f"실무 개발 분석 (수정 파일 목록, 구현 단계, 의존성 등):"
    )
    res2 = await ollama.chat(model=base_model, messages=[{"role": "user", "content": stage2_prompt}], temperature=0.2)
    stage2_out = res2.get("answer", "Stage 2 Failed")

    print("[Pipeline] Starting Stage 3: Final Instruction Consolidation")
    stage3_prompt = (
        f"당신은 테크 리드입니다. 1, 2단계 평가를 종합하여, 실제 On-Premise AI(예: Qwen 등)가 바로 코드를 작성할 수 있도록 완벽한 1개의 '최종 개발 지침(Instruction)' 마크다운을 작성하세요.\n"
        f"반드시 한국어로 작성하고, 마크다운 형식으로 정리하세요.\n\n"
        f"## Stage 1 Analysis:\n{stage1_out}\n\n"
        f"## Stage 2 Analysis:\n{stage2_out}\n\n"
        f"## Original Request:\n{user_request}\n\n"
        f"최종 개발 지침 (목표, 수정 대상 파일, 제약 조건, 상세 구현 지시):"
    )
    res3 = await ollama.chat(model=base_model, messages=[{"role": "user", "content": stage3_prompt}], temperature=0.2)
    stage3_out = res3.get("answer", "Stage 3 Failed")
    
    print("[Pipeline] 3-Stage Pipeline Completed")
    
    final_output = (
        "## [3-Stage Pipeline Result]\n"
        "> 이 지침은 3단계 사전 평가(구조->실무->최종)를 거쳐 정제된 최종 명령입니다.\n"
        "이 지침에 따라 코드를 작성하세요.\n\n"
        f"{stage3_out}"
    )
    return final_output
