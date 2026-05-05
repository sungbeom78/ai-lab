"""
instruction_review.py
- 3단계 지침 평가 실행
- Stage 1/2/3 순서로 Google AI (gemini) 또는 local-only 모드 지원
- 각 단계 결과를 파일로 저장
"""

import os
import json
import re
from datetime import datetime
from typing import Optional

from . import review_prompt_builder

# Google AI SDK (google-genai — 신규 버전)
try:
    from google import genai as google_genai
    GOOGLE_AI_AVAILABLE = True
except ImportError:
    GOOGLE_AI_AVAILABLE = False

# 결과 저장 기본 경로
OUT_BASE = "/project/ai-hub/out/instruction-review"

# 모델 설정 (사용자 지정)
# Stage 1: Gemini 2.5 Flash (구조 정리)
# Stage 2: Gemini 2.5 Flash (실전 개발 검증)
# Stage 3: Gemini 2.5 Pro (최종 승인)
GOOGLE_MODELS = {
    "stage1": "gemini-2.5-flash-preview-05-20",
    "stage2": "gemini-2.5-flash-preview-05-20",
    "stage3": "gemini-2.5-pro-preview-05-06",
}


def _safe_id_part(text: str, max_len: int = 20) -> str:
    """파일명에 사용 가능한 문자열로 변환."""
    return re.sub(r"[^a-zA-Z0-9_\-]", "_", text)[:max_len]


def _make_review_id(target_project: str) -> str:
    ts = datetime.now().strftime("%Y%m%d_%H%M%S")
    proj = _safe_id_part(target_project)
    return f"ir_{ts}_{proj}"


def _call_google_ai(
    api_key: str,
    model_name: str,
    system_prompt: str,
    user_prompt: str,
    temperature: float = 0.2
) -> str:
    """Google AI API를 호출하여 응답을 반환한다. (google-genai SDK 사용)"""
    if not GOOGLE_AI_AVAILABLE:
        return "Error: google-genai 패키지가 설치되어 있지 않습니다. pip install google-genai"

    client = google_genai.Client(api_key=api_key)

    full_prompt = f"{system_prompt}\n\n{user_prompt}"

    response = client.models.generate_content(
        model=model_name,
        contents=full_prompt,
        config={
            "temperature": temperature,
            "max_output_tokens": 8192,
        }
    )
    return response.text


def _call_local_stub(stage: int, user_prompt: str) -> str:
    """local-only 모드: 실제 AI 호출 없이 구조 템플릿을 반환한다."""
    stage_names = {
        1: "Stage 1: 구조 정리",
        2: "Stage 2: 실전 개발 검증",
        3: "Stage 3: 최종 승인 (Developer Request)",
    }
    name = stage_names.get(stage, f"Stage {stage}")
    return (
        f"# {name}\n\n"
        f"> **[local-only 모드]** 실제 AI 평가가 수행되지 않았습니다.\n"
        f"> google-eval-required-later 모드로 변경하면 Google AI 평가가 실행됩니다.\n\n"
        f"## 입력 요약\n\n"
        f"{user_prompt[:500]}...\n\n"
        f"## 평가 결과\n\n"
        f"- 실제 평가를 위해서는 `reviewer_mode`를 `google-eval-required-later`로 설정하세요.\n"
        f"- Google API key가 필요합니다.\n"
    )


def run_review(
    title: str,
    target_project: str,
    request_type: str,
    draft_instruction: str,
    reviewer_mode: str = "local-only",
    temperature: float = 0.2,
    google_api_key: Optional[str] = None,
) -> dict:
    """
    3단계 지침 평가를 실행하고 결과를 파일로 저장한다.

    Args:
        title: 평가 제목
        target_project: 대상 프로젝트
        request_type: 요청 유형
        draft_instruction: 초안 지침
        reviewer_mode: 'local-only' | 'google-eval-required-later'
        temperature: 생성 온도
        google_api_key: Google AI API key (google-eval 모드에서만 사용)

    Returns:
        review_id, 각 stage 파일 경로, metadata 경로 포함 dict
    """
    review_id = _make_review_id(target_project)
    review_dir = os.path.join(OUT_BASE, review_id)
    os.makedirs(review_dir, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    use_google = (
        reviewer_mode == "google-eval-required-later"
        and google_api_key
        and GOOGLE_AI_AVAILABLE
    )

    # Stage 1
    sys1, user1 = review_prompt_builder.build_stage1_prompt(
        title, target_project, request_type, draft_instruction
    )
    if use_google:
        stage1_result = _call_google_ai(
            google_api_key, GOOGLE_MODELS["stage1"], sys1, user1, temperature
        )
    else:
        stage1_result = _call_local_stub(1, user1)

    # Stage 2
    sys2, user2 = review_prompt_builder.build_stage2_prompt(
        title, target_project, request_type, stage1_result
    )
    if use_google:
        stage2_result = _call_google_ai(
            google_api_key, GOOGLE_MODELS["stage2"], sys2, user2, temperature
        )
    else:
        stage2_result = _call_local_stub(2, user2)

    # Stage 3
    sys3, user3 = review_prompt_builder.build_stage3_prompt(
        title, target_project, request_type, stage2_result
    )
    if use_google:
        stage3_result = _call_google_ai(
            google_api_key, GOOGLE_MODELS["stage3"], sys3, user3, temperature
        )
    else:
        stage3_result = _call_local_stub(3, user3)

    # 파일 저장
    v1_path = os.path.join(review_dir, "v1_original.md")
    v2_path = os.path.join(review_dir, "v2_stage1_structure_review.md")
    v3_path = os.path.join(review_dir, "v3_stage2_practical_review.md")
    v4_path = os.path.join(review_dir, "v4_stage3_final_approval.md")
    meta_path = os.path.join(review_dir, "review_metadata.json")
    summary_path = os.path.join(review_dir, "review_summary.md")

    with open(v1_path, "w", encoding="utf-8") as f:
        f.write(f"# 원본 초안\n\n제목: {title}\n대상: {target_project}\n유형: {request_type}\n\n---\n\n{draft_instruction}\n")

    with open(v2_path, "w", encoding="utf-8") as f:
        f.write(stage1_result)

    with open(v3_path, "w", encoding="utf-8") as f:
        f.write(stage2_result)

    with open(v4_path, "w", encoding="utf-8") as f:
        f.write(stage3_result)

    metadata = {
        "review_id": review_id,
        "title": title,
        "target_project": target_project,
        "request_type": request_type,
        "reviewer_mode": reviewer_mode,
        "temperature": temperature,
        "timestamp": timestamp,
        "google_ai_used": use_google,
        "models_used": GOOGLE_MODELS if use_google else {"all": "local-stub"},
        "status": "completed",
        "files": {
            "v1_original": v1_path,
            "v2_stage1": v2_path,
            "v3_stage2": v3_path,
            "v4_stage3": v4_path,
            "metadata": meta_path,
            "summary": summary_path,
        }
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    summary_content = f"""# Review Summary

- **Review ID**: {review_id}
- **제목**: {title}
- **대상 프로젝트**: {target_project}
- **요청 유형**: {request_type}
- **평가 모드**: {reviewer_mode}
- **Google AI 사용**: {use_google}
- **완료 시각**: {timestamp}

## Stage 결과 파일

| Stage | 파일 |
|-------|------|
| 원본 초안 | `v1_original.md` |
| Stage 1 구조 정리 | `v2_stage1_structure_review.md` |
| Stage 2 실전 검증 | `v3_stage2_practical_review.md` |
| Stage 3 최종 승인 | `v4_stage3_final_approval.md` |
"""

    with open(summary_path, "w", encoding="utf-8") as f:
        f.write(summary_content)

    return metadata
