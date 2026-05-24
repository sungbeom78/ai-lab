"""Session logger for OpenClaw Bridge Server.

Saves conversation sessions as Markdown files under workspace cache/openclaw/session/.
"""

import os
from datetime import datetime
from .config import SESSION_DIR


def generate_session_id() -> str:
    """Generate a session ID based on current timestamp."""
    return datetime.now().strftime("%Y%m%d_%H%M%S") + "_openclaw"


def get_session_dir(workspace_root: str) -> str:
    """Get the session log directory for a workspace, creating it if needed."""
    session_dir = os.path.join(workspace_root, SESSION_DIR)
    os.makedirs(session_dir, exist_ok=True)
    return session_dir


def save_session_log(
    workspace_root: str,
    session_id: str,
    user_message: str,
    instruction_path: str,
    active_file: str,
    selection: str,
    route: str,
    model: str,
    routing_reason: str,
    answer: str,
    mode: str = "develop",
    target_project: str = "",
    temperature: float = 0.2,
    enabled_tools: list[str] = None,
    evidence_files: list[str] = None,
) -> str:
    """Save a session log as a Markdown file.

    Returns:
        Absolute path to the saved log file.
    """
    session_dir = get_session_dir(workspace_root)
    log_path = os.path.join(session_dir, f"{session_id}.md")

    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    tools_str = ", ".join(enabled_tools) if enabled_tools else "(none)"
    evidence_str = "\n".join(f"- {f}" for f in (evidence_files or [])) or "(none)"

    content = f"""# OpenClaw Session Log

## Context

| Field | Value |
|-------|-------|
| **Session ID** | {session_id} |
| **Timestamp** | {timestamp} |
| **Workspace** | {workspace_root} |
| **Target Project** | {target_project or "(none)"} |
| **Mode** | {mode} |
| **Temperature** | {temperature} |
| **Enabled Tools** | {tools_str} |
| **Route** | {route} |
| **Model** | {model} |
| **Routing Reason** | {routing_reason} |

## User Request

- **Active File**: {active_file or "(none)"}
- **Instruction Path**: {instruction_path or "(none)"}
- **Selection**: {selection[:200] if selection else "(none)"}

### Message

{user_message}

## Evidence Files Referenced

{evidence_str}

## Response

{answer}

## Next Steps

(to be determined by follow-up interaction)

## Files Changed

(none — MVP: edit/execute require user approval)
"""

    with open(log_path, "w", encoding="utf-8") as f:
        f.write(content)

    return log_path
