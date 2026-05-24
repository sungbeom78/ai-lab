"""
lostway_conversation_log.py
Lostway 대화 기록 생성, 조회, 읽기 기능을 담당하는 모듈.
"""

import os
import re
import glob
from datetime import datetime

LOSTWAY_CONV_DIR = "/project/lostway/doc/conversation"

CONV_TYPE_LABELS = {
    "idea": "아이디어",
    "planning": "기획",
    "worldview": "세계관",
    "character": "캐릭터",
    "system": "시스템",
    "scenario": "시나리오",
    "review": "검토",
    "memo": "메모",
}


def _sanitize_filename_part(text: str) -> str:
    """파일명에 사용 불가한 문자를 _ 로 치환한다."""
    sanitized = re.sub(r'[\\/:*?"<>|]', "_", text)
    # 공백 및 한글 등 일반 slug 처리
    sanitized = re.sub(r"\s+", "_", sanitized)
    return sanitized.strip("_")


def _slug_from_title(title: str, max_len: int = 40) -> str:
    """제목에서 파일명용 slug 를 생성한다."""
    slug = _sanitize_filename_part(title)
    slug = re.sub(r"_+", "_", slug)
    return slug[:max_len]


def _ensure_conv_dir() -> None:
    """저장 디렉토리가 없으면 생성한다."""
    os.makedirs(LOSTWAY_CONV_DIR, exist_ok=True)


def _safe_path(filename: str) -> str:
    """path traversal 방어: 저장 경로가 LOSTWAY_CONV_DIR 하위인지 검증한다."""
    target = os.path.realpath(os.path.join(LOSTWAY_CONV_DIR, filename))
    base = os.path.realpath(LOSTWAY_CONV_DIR)
    if not target.startswith(base + os.sep):
        raise ValueError(f"Invalid filename: {filename}")
    return target


def _unique_path(base_path: str) -> str:
    """동일 파일명이 존재하면 _2, _3 ... suffix 를 붙여 유일한 경로를 반환한다."""
    if not os.path.exists(base_path):
        return base_path
    root, ext = os.path.splitext(base_path)
    counter = 2
    while True:
        candidate = f"{root}_{counter}{ext}"
        if not os.path.exists(candidate):
            return candidate
        counter += 1


def generate_filename(title: str, conv_type: str = "planning") -> str:
    """YYYYMMDD_HHMM_lostway_<slug>.md 형식의 파일명을 생성한다."""
    now = datetime.now()
    datestamp = now.strftime("%Y%m%d_%H%M")
    slug = _slug_from_title(title)
    # 'lostway' 접두사 중복 방지
    slug_lower = slug.lower()
    if slug_lower.startswith("lostway_"):
        slug = slug[8:]
    elif slug_lower == "lostway":
        slug = conv_type
    if not slug:
        slug = conv_type
    return f"{datestamp}_lostway_{slug}.md"


def build_markdown(
    title: str,
    date: str,
    participants: list[str],
    conv_type: str,
    tags: list[str],
    content: str,
    memo: str,
) -> str:
    """Markdown 대화 기록 파일 내용을 생성한다."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    type_label = CONV_TYPE_LABELS.get(conv_type, conv_type)
    participants_str = ", ".join(participants) if participants else "범이, AI"
    tags_str = ", ".join(tags) if tags else ""

    lines = [
        f"# {title}",
        "",
        "## Metadata",
        "",
        "| 항목 | 값 |",
        "|---|---|",
        "| Project | lostway |",
        f"| Date | {date} |",
        f"| Type | {type_label} |",
        f"| Participants | {participants_str} |",
        f"| Tags | {tags_str} |",
        f"| Created At | {now} |",
        "| Source | AI Hub Lostway Log |",
        "",
        "---",
        "",
        "## Summary",
        "",
    ]

    if memo and memo.strip():
        lines.append(memo.strip())
    else:
        lines.append("(요약 없음)")

    lines += [
        "",
        "---",
        "",
        "## Conversation",
        "",
        content.strip(),
        "",
        "---",
        "",
        "## Notes",
        "",
        "(추가 메모 없음)",
        "",
        "---",
        "",
        "## Follow-up Actions",
        "",
        "- [ ] 후속 작업이 있으면 기록한다.",
        "",
    ]

    return "\n".join(lines)


def save_conversation_log(
    title: str,
    content: str,
    date: str | None = None,
    participants: list[str] | None = None,
    conv_type: str = "planning",
    tags: list[str] | None = None,
    memo: str = "",
    filename: str = "",
) -> dict:
    """대화 기록을 Markdown 파일로 저장하고 결과 dict 를 반환한다."""
    # 유효성 검증
    if not title or not title.strip():
        raise ValueError("title 은 필수값입니다.")
    if not content or not content.strip():
        raise ValueError("content 는 필수값입니다.")
    if len(title) > 200:
        raise ValueError("title 은 200자 이내여야 합니다.")
    if len(content) > 200_000:
        raise ValueError("content 는 200,000자 이내여야 합니다.")

    # 날짜 기본값
    if not date:
        date = datetime.now().strftime("%Y-%m-%d")

    # 참여자 기본값
    if not participants:
        participants = ["범이", "AI"]

    # 태그 기본값
    if tags is None:
        tags = []

    # 파일명 처리
    if filename and filename.strip():
        safe_name = _sanitize_filename_part(filename.strip())
        if not safe_name.endswith(".md"):
            safe_name += ".md"
        if len(safe_name) > 150:
            raise ValueError("filename 은 150자 이내여야 합니다.")
    else:
        safe_name = generate_filename(title, conv_type)

    _ensure_conv_dir()
    target_path = _safe_path(safe_name)
    target_path = _unique_path(target_path)
    final_filename = os.path.basename(target_path)

    md_content = build_markdown(
        title=title,
        date=date,
        participants=participants,
        conv_type=conv_type,
        tags=tags,
        content=content,
        memo=memo,
    )

    with open(target_path, "w", encoding="utf-8") as f:
        f.write(md_content)

    return {
        "ok": True,
        "path": target_path,
        "filename": final_filename,
    }


def list_conversation_logs(limit: int = 30) -> list[dict]:
    """최근 대화 기록 파일 목록을 반환한다."""
    if not os.path.exists(LOSTWAY_CONV_DIR):
        return []

    files = glob.glob(os.path.join(LOSTWAY_CONV_DIR, "*.md"))
    files.sort(key=os.path.getmtime, reverse=True)

    items = []
    for f in files[:limit]:
        mtime = os.path.getmtime(f)
        created_at = datetime.fromtimestamp(mtime).strftime("%Y-%m-%d %H:%M:%S")
        items.append({
            "filename": os.path.basename(f),
            "path": f,
            "createdAt": created_at,
        })
    return items


def read_conversation_log(filename: str) -> str:
    """지정한 대화 기록 파일의 내용을 반환한다. path traversal 방어 포함."""
    # 파일명만 허용 (디렉토리 구분자 금지)
    if not re.match(r"^[a-zA-Z0-9_\-가-힣\.]+$", filename):
        raise ValueError(f"Invalid filename: {filename}")
    target_path = _safe_path(filename)
    if not os.path.isfile(target_path):
        raise FileNotFoundError(f"File not found: {filename}")
    with open(target_path, "r", encoding="utf-8") as f:
        return f.read()
