"""
developer_request_writer.py
- Stage 3 최종 결과를 opai 개발자에게 전달 가능한 문서로 변환
- 실행 범위, 금지 사항, 검증 명령, 기록 위치 포함
"""

import os
import json
from datetime import datetime

OUT_BASE = "/project/ai-hub/out/developer-request"


def write_developer_request(
    review_id: str,
    title: str,
    target_project: str,
    request_type: str,
    stage3_result: str,
    reviewer_mode: str = "local-only",
) -> dict:
    """
    Stage 3 결과를 opai Developer Request 문서로 저장한다.

    Args:
        review_id: 연결된 instruction review ID
        title: 요청 제목
        target_project: 대상 프로젝트
        request_type: 요청 유형
        stage3_result: Stage 3 최종 평가 결과 (FULL REWRITE 텍스트)
        reviewer_mode: 평가 모드

    Returns:
        저장된 파일 경로 dict
    """
    os.makedirs(OUT_BASE, exist_ok=True)

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    request_id = review_id  # review_id를 그대로 사용

    doc_path = os.path.join(OUT_BASE, f"{request_id}_opai_developer_request.md")
    meta_path = os.path.join(OUT_BASE, f"{request_id}_opai_developer_request_metadata.json")

    doc_content = f"""# Developer Request

> **작성 시각**: {timestamp}
> **Review ID**: {review_id}
> **제목**: {title}
> **대상 프로젝트**: {target_project}
> **요청 유형**: {request_type}
> **평가 모드**: {reviewer_mode}
> **Status**: ready_for_opai

---

{stage3_result}

---

## 전달 정보

- **원본 리뷰 디렉터리**: `/project/ai-hub/out/instruction-review/{review_id}/`
- **Developer Request 파일**: `{doc_path}`
- **작업 완료 후 Status를 `completed`로 변경 요청**
"""

    with open(doc_path, "w", encoding="utf-8") as f:
        f.write(doc_content)

    metadata = {
        "request_id": request_id,
        "review_id": review_id,
        "title": title,
        "target_project": target_project,
        "request_type": request_type,
        "reviewer_mode": reviewer_mode,
        "timestamp": timestamp,
        "status": "ready_for_opai",
        "doc_path": doc_path,
        "meta_path": meta_path,
    }

    with open(meta_path, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

    return {
        "request_id": request_id,
        "doc_path": doc_path,
        "meta_path": meta_path,
        "status": "ready_for_opai",
    }


def list_developer_requests(limit: int = 20) -> list[dict]:
    """
    Developer Request 목록을 최신순으로 반환한다.
    """
    if not os.path.exists(OUT_BASE):
        return []

    results = []
    for fname in sorted(os.listdir(OUT_BASE), reverse=True):
        if fname.endswith("_opai_developer_request_metadata.json"):
            fpath = os.path.join(OUT_BASE, fname)
            try:
                with open(fpath, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                results.append(meta)
            except Exception:
                continue
        if len(results) >= limit:
            break

    return results


def get_developer_request(request_id: str) -> dict | None:
    """
    특정 Developer Request 메타데이터를 반환한다. (path traversal 방어 포함)
    """
    import re
    if not re.match(r"^[a-zA-Z0-9_\-]+$", request_id):
        return None

    meta_path = os.path.join(OUT_BASE, f"{request_id}_opai_developer_request_metadata.json")
    doc_path = os.path.join(OUT_BASE, f"{request_id}_opai_developer_request.md")

    # path traversal 방어
    real_meta = os.path.realpath(meta_path)
    real_base = os.path.realpath(OUT_BASE)
    if not real_meta.startswith(real_base):
        return None

    if not os.path.isfile(meta_path):
        return None

    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)

    if os.path.isfile(doc_path):
        with open(doc_path, "r", encoding="utf-8") as f:
            meta["doc_content"] = f.read()

    return meta
