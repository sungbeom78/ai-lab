"""Instruction file handler for OpenClaw Bridge Server.

Reads instruction files and builds context for LLM processing.
"""

import os


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


def build_system_prompt(
    workspace_root: str,
    instruction_content: str = "",
    active_file_content: str = "",
    active_file_name: str = "",
    selection: str = "",
) -> str:
    """Build a system prompt with all available context.

    Args:
        workspace_root: Root path of the workspace.
        instruction_content: Content of the instruction file, if any.
        active_file_content: Content of the active editor file.
        active_file_name: Name of the active file.
        selection: Selected text in the editor.

    Returns:
        Formatted system prompt string.
    """
    parts = []

    parts.append(f"You are OpenClaw, a locally hosted, independent AI coding assistant operating within the workspace at: {workspace_root}")
    parts.append("You are powered by local open-source models like Gemma or Qwen via Ollama, not by Google's cloud APIs.")
    parts.append("CRITICAL RULE: You must NEVER claim to be Gemini, Google, OpenAI, or any cloud-based AI. Your identity is strictly 'OpenClaw'.")
    parts.append("You help with code development, analysis, planning, and documentation.")
    parts.append("Respond in Korean unless the user writes in English.")
    parts.append("")

    if instruction_content:
        parts.append("## Instruction File")
        parts.append("")
        parts.append(instruction_content)
        parts.append("")

    if active_file_content:
        parts.append(f"## Currently Open File: {active_file_name}")
        parts.append("")
        parts.append("```")
        parts.append(active_file_content)
        parts.append("```")
        parts.append("")

    if selection:
        parts.append("## Selected Text")
        parts.append("")
        parts.append("```")
        parts.append(selection)
        parts.append("```")
        parts.append("")

    return "\n".join(parts)
