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

_MODE_DIRECTIVES = {
    "inspect": """[INSPECT MODE DIRECTIVE]
- 대상 소스 코드, 프로젝트 구조, 요구사항 및 로그를 철저히 파악하고 면밀히 조사하십시오.
- 단순 코드 훑어보기에 그치지 않고, 의존 관계와 아키텍처 결합도 측면에서 구조적 통찰을 도출하십시오.""",
    "prepare": """[PREPARE MODE DIRECTIVE]
- 변경을 시작하기 전, 구체적인 구현 계획(Implementation Plan), 상세 To-Do 단계 및 예상 산출물 목록을 정의하십시오.
- 잠재적인 부작용 범위와 사전 준비 작업들을 명확히 나열하십시오.""",
    "develop": """[DEVELOP MODE DIRECTIVE - CRITICAL RULE]
- 당신은 현재 'develop(개발/수정)' 모드로 동작 중입니다.
- **[요약 금지 법칙] 절대로 변경 사항이나 해결책을 대략적인 개념 설명이나 말로 요약만 하고 응답을 끝마치지 마십시오.**
- **반드시 '## Proposed Files' 또는 이에 준하는 수정 대상 코드 섹션에 카피하여 즉시 파일에 반영할 수 있는 완전하고 완성도 높은 소스 코드(또는 완벽한 패치형 diff)를 한 줄도 생략 없이 구체적으로 작성해야 합니다.**
- 코드 중간을 주석(`// ... 기존 로직 ...` 등)으로 날려버리거나 채워 넣기를 미루는 중략 행위를 극도로 금지합니다. 동작 가능한 완전한 형태로 구현하십시오.""",
    "validate": """[VALIDATE MODE DIRECTIVE]
- 구현 사항을 완벽하게 검증하기 위한 테스트 계획, 유닛 테스트 스크립트 작성 예시, 그리고 터미널에서 실행할 정확한 빌드/테스트 명령 목록을 제공하십시오.
- 발생 가능한 엣지 케이스들을 점검하는 명확한 검증 체크리스트를 제안하십시오.""",
    "operate": """[OPERATE MODE DIRECTIVE]
- 서비스의 안전한 배포 및 기동 가이드, 환경 설정 튜닝, 모니터링 기법, 그리고 장애 대응 롤백(Rollback) 시나리오를 설계하십시오."""
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
    modes = [m.strip().lower() for m in mode.split(',')] if mode else ["develop"]
    has_develop = "develop" in modes
    
    parts.append("## Current Mode & Action Directives")
    for m in modes:
        desc = _MODE_DESCRIPTIONS.get(m, f"모드: {m}")
        parts.append(f"### Mode: **{m}**")
        parts.append(f"- {desc}")
        
        # [CRITICAL MERGE RULE] 만약 다중 모드 중 develop(개발)이 단 하나라도 포함되어 있다면,
        # inspect나 prepare의 '계획 및 요약만 해라'는 제약은 자동으로 해제되며,
        # 무조건 Proposed Files 코드 작성을 완료해야 하는 develop 지침이 최상위 우선권(Override)을 가집니다.
        if m in ("inspect", "prepare") and has_develop:
            parts.append("*(주의: 현재 Develop(개발) 모드가 함께 켜져 있으므로, 요약/스캔 보고서 작성에 그치지 말고 본문의 코딩 규격에 맞추어 실제 Proposed Files 소스코드 완성을 무조건 1순위로 진행하십시오.)*")
            if m == "inspect":
                parts.append("[INSPECT DIRECTIVE - DEVELOP OVERRIDE]\n- 대상 파일 구조를 속성으로 스캔하되, 바로Proposed Files에 온전한 코드를 작성해 넣으십시오.")
            elif m == "prepare":
                parts.append("[PREPARE DIRECTIVE - DEVELOP OVERRIDE]\n- 문서 계획만 작성하지 마시고, 실제 카피 가능한 완성본 코드를 패치 블록에 반드시 포함하십시오.")
        else:
            if m in _MODE_DIRECTIVES:
                parts.append(_MODE_DIRECTIVES[m])
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
            
        # [MANDATORY] 자동 실행 포맷 가이드 주입
        parts.append("")
        parts.append("### [TOOL AUTO-EXECUTION FORMAT RULES]")
        parts.append("사용자가 귀하에게 'edit' 또는 'execute' 권한을 활성화하여 질의했습니다. 귀하의 코드 블록 응답은 백엔드 실행 파서에 의해 **실제 로컬 파일에 즉시 쓰이거나 터미널에 자동 실행**됩니다.")
        parts.append("이 실시간 자동 반영 작업을 위해 반드시 아래의 양식을 엄격하고 완벽하게 지켜 코드를 작성하십시오:")
        
        if "edit" in enabled_tools:
            parts.append("1. **파일 생성/수정 (edit 권한 활성화 상태)**:")
            parts.append("   - 수정하거나 생성할 파일 내용을 마크다운 코드 블록 안에 넣으십시오.")
            parts.append("   - **반드시 코드 블록의 첫 번째 라인에 언어 문법에 맞는 주석 기호를 적고 `### FILE: <file_absolute_path>` 형식의 파일 주석을 한 줄 명시하십시오. (중요)**")
            parts.append("   - 코드 내부에 '// ... 기존 코드 ...' 식의 로직 생략 주석을 적는 일을 엄격히 금지합니다. 소스 코드를 온전하게 완성하십시오.")
            parts.append("   - 예시 (JavaScript):")
            parts.append("     ```javascript")
            parts.append("     // ### FILE: /project/site/ahnda/assets/js/app.js")
            parts.append("     console.log('App loaded successfully.');")
            parts.append("     ```")
            parts.append("   - 예시 (Python):")
            parts.append("     ```python")
            parts.append("     # ### FILE: /project/ai-hub/app/openclaw/test.py")
            parts.append("     print('Test file successfully created.')")
            parts.append("     ```")
            
        if "execute" in enabled_tools:
            parts.append("2. **명령어 실행 (execute 권한 활성화 상태)**:")
            parts.append("   - 실행할 터미널 명령어는 bash/sh 코드 블록 안에 넣으십시오.")
            parts.append("   - **반드시 첫 번째 라인에 `### CMD:`를 주석으로 명시하십시오.**")
            parts.append("   - 예시:")
            parts.append("     ```bash")
            parts.append("     # ### CMD:")
            parts.append("     npm run compile")
            parts.append("     ```")
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
    
    has_develop = "develop" in modes
    has_validate = "validate" in modes
    
    if has_develop or has_validate:
        parts.append("- **Proposed Files (수정 대상 파일)**: 정확한 파일 경로와 카피 가능한 전체 완성 소스 코드 (develop 모드일 때 특히 필수, 중략 불가)")
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
        parts.append("## Instruction File [CRITICAL / ABSOLUTE RULE - NO JUDGMENT]")
        parts.append("아래에 로드된 기획 지침 파일(Instruction / Specification File)은 귀하가 이번 작업에서 한 치의 오차도 없이 100% 똑같이 구현해 내야 하는 **절대적인 개발 명세서(Absolute Development Specification)**입니다.")
        parts.append("귀하는 이 기획안에 대해 어떠한 주관적인 '다음 작업 판단', '타당성 분석', '요약 보고 및 계획 수립' 등의 중간 행위를 절대 개입시켜서는 안 되며, 오로지 이 명세서에 지시된 UI 정보(이력서 정보 등), 레이아웃 가이드 및 파일 생성/수정 요구사항 그대로 **실제 가용하고 완성된 소스코드를 Proposed Files 코드 블록에 단 한 줄의 중략 생략도 없이 즉시 100% 완벽하게 작성해야만 합니다.**")
        parts.append("기획서가 주어졌음에도 코드를 작성하지 않고 '분석만 하고 멈추는 행위'나 '말로 때우며 파일 수정 출력을 누락하는 행위'는 귀하의 시스템 기동 실패 및 항명으로 간주됩니다. 귀하는 오로지 명세서의 명령 그대로 index.html 등의 관련 대상 파일을 즉각적이고 물리적으로 완성하는 완전 자동화 기계(Execution Engine)로서 충실히 동작해야 합니다.")
        parts.append("```markdown")
        parts.append(instruction_content)
        parts.append("```")
        
        if has_develop:
            parts.append("")
            parts.append("### [CRITICAL FORMAT RESOLUTION DIRECTIVE]")
            parts.append("IMPORTANT: 기획 지침 파일의 끝부분에 '작업이 끝난 뒤에는 아래 형식으로만 답한다' 또는 '~라고만 말하고 멈춰라' 등의 엄격한 응답 템플릿 제약이 기재되어 있을 수 있습니다.")
            parts.append("그러나 귀하는 현재 **develop(개발/수정)** 모드로 동작하고 있으므로, 파일에 실제 수정 사항을 물리적으로 반영하고 에디터에 자동 덮어쓰기 위해 **반드시 완전한 소스 코드가 포함된 `### FILE: <file_absolute_path>` 형식의 마크다운 코드 블록(Proposed Files)을 본문 내에 절대로 한 줄의 생략도 없이 완성도 높게 먼저 출력해야만 합니다!**")
            parts.append("기획서의 템플릿 제약은 코드 블록 출력이 끝난 **맨 마지막 부분에 부록(Appendix) 형태로 반드시 기재**하십시오. 본문 내 소스 코드 블록을 절대 누락하거나 요약하지 마십시오. 코드를 생략하여 요약문만 출력하면 자동 에디터 쓰기 엔진이 동작하지 않아 치명적인 실패가 유발됩니다.")
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
