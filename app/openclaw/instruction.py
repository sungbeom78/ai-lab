"""Instruction file handler for OpenClaw Bridge Server.

Reads instruction files and builds context for LLM processing.
"""

import os
import glob
from pathlib import Path


def read_instruction_file(instruction_path: str) -> dict:
    """Read and parse an instruction file.

    Args:
        instruction_path: Absolute path to the instruction file.

    Returns:
        dict with "ok", "content", "filename", and optionally "error".
    """
    if not instruction_path:
        return {"ok": False, "content": "", "filename": "", "error": "No instruction path provided"}

    if not os.path.isfile(instruction_path):
        return {"ok": False, "content": "", "filename": instruction_path, "error": f"File not found: {instruction_path}"}

    try:
        with open(instruction_path, "r", encoding="utf-8") as f:
            content = f.read()
        return {
            "ok": True,
            "content": content,
            "filename": os.path.basename(instruction_path),
            "size": len(content),
        }
    except Exception as e:
        return {"ok": False, "content": "", "filename": instruction_path, "error": str(e)}


def read_active_file(file_path: str, max_lines: int = 200) -> dict:
    """Read the currently active file in the editor.

    Args:
        file_path: Absolute path to the active file.
        max_lines: Maximum number of lines to include.

    Returns:
        dict with file content summary.
    """
    if not file_path:
        return {"ok": False, "content": "", "error": "No active file"}

    if not os.path.isfile(file_path):
        return {"ok": False, "content": "", "error": f"File not found: {file_path}"}

    try:
        with open(file_path, "r", encoding="utf-8") as f:
            lines = f.readlines()

        total_lines = len(lines)
        truncated = total_lines > max_lines
        content = "".join(lines[:max_lines])

        return {
            "ok": True,
            "content": content,
            "filename": os.path.basename(file_path),
            "total_lines": total_lines,
            "truncated": truncated,
        }
    except Exception as e:
        return {"ok": False, "content": "", "error": str(e)}


def get_workspace_tree(workspace_root: str, max_depth: int = 3) -> str:
    """Generate a tree representation of the workspace."""
    if not workspace_root or not os.path.isdir(workspace_root):
        return f"Cannot scan workspace: invalid path {workspace_root}"

    ignore_dirs = {".git", "node_modules", ".venv", "venv", "__pycache__", "dist", "build", "out"}
    tree_lines = []

    def scan_dir(current_path, current_depth, prefix=""):
        if current_depth > max_depth:
            return
        
        try:
            entries = sorted(os.listdir(current_path))
        except PermissionError:
            return

        dirs = []
        files = []
        for entry in entries:
            if entry in ignore_dirs:
                continue
            full_path = os.path.join(current_path, entry)
            if os.path.isdir(full_path):
                dirs.append(entry)
            else:
                files.append(entry)

        for i, d in enumerate(dirs):
            is_last = (i == len(dirs) - 1) and (len(files) == 0)
            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{connector}{d}/")
            extension = "    " if is_last else "│   "
            scan_dir(os.path.join(current_path, d), current_depth + 1, prefix + extension)

        for i, f in enumerate(files):
            is_last = (i == len(files) - 1)
            connector = "└── " if is_last else "├── "
            tree_lines.append(f"{prefix}{connector}{f}")

    tree_lines.append(os.path.basename(workspace_root) + "/")
    scan_dir(workspace_root, 1)
    
    # Check for important files
    important_files = ["README.md", "package.json", "pyproject.toml", "requirements.txt", "workspace.yaml", "PROJECT_CHARTER.md"]
    found_important = []
    for imp in important_files:
        if os.path.isfile(os.path.join(workspace_root, imp)):
            found_important.append(imp)

    tree_str = "\n".join(tree_lines[:200])  # limit to avoid huge trees
    if len(tree_lines) > 200:
        tree_str += "\n... (truncated)"
        
    return f"Important files found: {', '.join(found_important)}\n\nTree:\n{tree_str}"

def get_recent_logs(workspace_root: str) -> str:
    """Read recent files from session, log, and doc/plan dirs."""
    log_content = []
    search_dirs = [
        "cache/openclaw/session",
        "log",
        "doc/plan"
    ]
    
    for d in search_dirs:
        full_dir = os.path.join(workspace_root, d)
        if not os.path.isdir(full_dir):
            continue

        files = sorted(glob.glob(os.path.join(full_dir, "*.md")), key=os.path.getmtime, reverse=True)
        for f in files[:3]:
            try:
                with open(f, "r", encoding="utf-8") as fp:
                    preview = fp.read(500)
                log_content.append(f"### {os.path.basename(f)}\n{preview}...")
            except Exception:
                pass
            
    if not log_content:
        return "No recent logs found."
    return "\n\n".join(log_content)


# File extension → language mapping for activeFile type detection
_EXT_LANG = {
    ".py": "Python/FastAPI",
    ".ts": "TypeScript",
    ".tsx": "TypeScript/React",
    ".js": "JavaScript",
    ".jsx": "JavaScript/React",
    ".vue": "Vue.js",
    ".svelte": "Svelte",
    ".go": "Go",
    ".rs": "Rust",
    ".java": "Java",
    ".kt": "Kotlin",
    ".rb": "Ruby",
    ".php": "PHP",
    ".cs": "C#",
    ".cpp": "C++",
    ".c": "C",
    ".sh": "Shell Script",
    ".md": "Markdown",
    ".json": "JSON",
    ".yaml": "YAML",
    ".yml": "YAML",
    ".toml": "TOML",
    ".html": "HTML",
    ".css": "CSS",
}


def _detect_file_language(filename: str) -> str:
    ext = os.path.splitext(filename)[1].lower()
    return _EXT_LANG.get(ext, f"Unknown ({ext})")


_MODE_DESCRIPTIONS = {
    "inspect": "분석/조사 모드: 파일과 구조, 요구사항을 분석하고 변경 제안까지만 합니다. 실제 코드 수정은 하지 않습니다.",
    "prepare": "준비/계획 모드: 작업 계획, 우선순위, 산출물 정의를 중심으로 응답합니다.",
    "develop": "개발/수정 모드: 수정 대상 파일, 구현 순서, patch 제안을 중심으로 응답합니다.",
    "validate": "검증/테스트 모드: 테스트 명령, 검증 기준, 실패 조건을 중심으로 응답합니다.",
    "operate": "운영/배포 모드: 실행, 배포, 모니터링, 롤백 기준을 중심으로 응답합니다.",
}

_TOOL_DESCRIPTIONS = {
    "read":    ("워크스페이스 내 파일 읽기 및 탐색", "activeFile, instructionPath, 관련 문서 읽기 가능"),
    "search":  ("워크스페이스 내 파일 검색", "관련 파일/로그 찾기 가능"),
    "edit":    ("워크스페이스 내 파일 수정 제안", "patch 제안 가능 (실제 저장 전 사용자 승인 필요)"),
    "execute": ("터미널 명령 실행 계획 제안", "명령어 제안 가능 (실제 실행 전 사용자 승인 필요)"),
    "browser": ("웹 브라우저를 통한 인터넷 탐색", "현재 MVP에서는 안내 및 계획만 가능"),
}


def build_system_prompt(
    workspace_root: str,
    instruction_content: str = "",
    active_file_content: str = "",
    active_file_name: str = "",
    active_file_path: str = "",
    selection: str = "",
    tools: list[str] = None,
    mode: str = "develop",
    target_project: str = "",
    temperature: float = 0.2,
) -> str:
    """Build a comprehensive system prompt with all available context.

    Args:
        workspace_root: Root path of the workspace.
        instruction_content: Content of the instruction file, if any.
        active_file_content: Content of the active editor file.
        active_file_name: Name of the active file (basename).
        active_file_path: Full path to the active file.
        selection: Selected text in the editor.
        tools: List of enabled tool names.
        mode: Work mode (inspect/prepare/develop/validate/operate).
        target_project: Selected project name from dropdown.
        temperature: LLM temperature setting.

    Returns:
        Formatted system prompt string.
    """
    parts = []

    # ── Identity ─────────────────────────────────────────────────────────────
    parts.append(f"You are OpenClaw, a locally hosted, independent AI coding assistant.")
    parts.append(f"Workspace: {workspace_root}")
    if target_project:
        parts.append(f"Target Project: {target_project}")
    parts.append("You are powered by local open-source models (Gemma/Qwen via Ollama). NOT Google, NOT OpenAI.")
    parts.append("CRITICAL: NEVER claim to be Gemini, Google, OpenAI or any cloud AI. Your identity is strictly 'OpenClaw'.")
    parts.append("Respond in Korean unless the user writes in English.")
    parts.append("")

    # ── Mode ─────────────────────────────────────────────────────────────────
    mode_desc = _MODE_DESCRIPTIONS.get(mode, f"모드: {mode}")
    parts.append("## Current Mode")
    parts.append(f"**{mode}** — {mode_desc}")
    parts.append("")

    # ── Configure Tools ───────────────────────────────────────────────────────
    enabled_tools = tools or []
    disabled_tools = [t for t in _TOOL_DESCRIPTIONS if t not in enabled_tools]

    parts.append("## Available Tools & Capabilities")
    if enabled_tools:
        parts.append("다음 도구를 사용할 수 있는 권한이 있습니다. 필요한 경우 답변에 **순차 실행 계획**으로 명시하십시오.")
        for t in enabled_tools:
            short, detail = _TOOL_DESCRIPTIONS.get(t, (t, ""))
            parts.append(f"- **{t}** ✅: {short} ({detail})")
    if disabled_tools:
        parts.append("다음 도구는 **비활성화** 되어 있습니다. 해당 도구를 통한 작업을 수행했다고 말하지 마십시오.")
        for t in disabled_tools:
            short, _ = _TOOL_DESCRIPTIONS.get(t, (t, ""))
            parts.append(f"- **{t}** ❌: {short}")
    parts.append("")

    # ── Internal Quality Loop Instructions ────────────────────────────────────
    parts.append("## Internal Quality Rules (MANDATORY)")
    parts.append("최종 응답 전 반드시 내부적으로 다음을 검토하십시오:")
    parts.append("1. Context Collect: workspaceRoot, activeFile, instructionPath, recentLogs 수집 확인")
    parts.append("2. Evidence Summary: 실제 읽은 파일/경로만 근거로 사용")
    parts.append("3. Tool Capability Check: enabledTools에 없는 작업을 수행했다고 말하지 않는다")
    parts.append("4. Self Review:")
    parts.append("   - 실제 읽지 않은 파일을 읽었다고 말했는가?")
    parts.append("   - 없는 파일/경로를 지어냈는가?")
    parts.append("   - activeFile 언어/타입을 잘못 판단했는가?")
    parts.append("   - instructionPath 내용을 일반론으로 대체했는가?")
    parts.append("   - enabledTools에 없는 기능을 수행했다고 말했는가?")
    parts.append("5. Final Answer: 아래 응답 형식을 최대한 따른다")
    parts.append("")

    # ── Response Format ───────────────────────────────────────────────────────
    parts.append("## Response Format")
    parts.append("가능하면 다음 구조를 따르십시오:")
    parts.append("- **요약**: 무엇을 파악/수행했는가")
    parts.append("- **근거**: 실제 읽은 파일, 경로, 내용 기반")
    parts.append("- **판단**: 현재 상태 평가")
    parts.append("- **다음 작업**: 우선순위 순서로")
    parts.append("- **주의사항**: 금지/보류/위험 항목")
    if mode in ("develop", "validate"):
        parts.append("- **수정 대상 파일**: 정확한 경로")
        parts.append("- **검증 명령**: 실제 실행 가능한 명령")
    parts.append("")

    # ── Workspace Structure ────────────────────────────────────────────────────
    parts.append("## Workspace Structure")
    parts.append("```text")
    parts.append(get_workspace_tree(workspace_root))
    parts.append("```")
    parts.append("")

    # ── Active File ────────────────────────────────────────────────────────────
    parts.append("## Active File Context")
    if active_file_content and active_file_name:
        detected_lang = _detect_file_language(active_file_name)
        parts.append(f"Currently open file: **{active_file_name}** (언어: {detected_lang})")
        parts.append(f"IMPORTANT: 이 파일의 실제 언어는 **{detected_lang}** 입니다. 사용자 질문이 다른 언어를 언급하더라도 실제 파일 기준으로 판단하십시오.")
        parts.append(f"```{detected_lang.split('/')[0].lower()}")
        parts.append(active_file_content)
        parts.append("```")
    else:
        parts.append("No active file was provided or it could not be read. Do NOT claim you analyzed an active file.")
    parts.append("")

    # ── Instruction File Analysis ─────────────────────────────────────────────
    if instruction_content:
        parts.append("## Instruction File Analysis")
        parts.append("아래 지침 파일을 실제로 읽었습니다. 다음 구조로 핵심 요구사항을 추출하여 응답을 구성하십시오:")
        parts.append("(작업 목표 / 대상 프로젝트 / 작업 범위 / 현재 완료된 것 / 다음 작업 / 수정 대상 파일 / 신규 생성 파일 / 금지·보류 / 검증 기준)")
        parts.append("일반론으로 대체하지 말고 지침 파일의 실제 내용을 기반으로 구체적으로 답변하십시오.")
        parts.append("```markdown")
        parts.append(instruction_content)
        parts.append("```")
        parts.append("")

    # ── Selection ─────────────────────────────────────────────────────────────
    if selection:
        parts.append("## Selected Text Priority")
        parts.append("사용자가 명시적으로 선택한 텍스트입니다. 이 컨텍스트를 최우선으로 사용하십시오:")
        parts.append("```")
        parts.append(selection)
        parts.append("```")
        parts.append("")

    # ── Recent Logs ────────────────────────────────────────────────────────────
    parts.append("## Recent Session Logs")
    parts.append("```text")
    parts.append(get_recent_logs(workspace_root))
    parts.append("```")
    parts.append("")

    return "\n".join(parts)
