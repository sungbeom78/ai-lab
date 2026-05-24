"""OpenClaw Auto Execution Engine.

Parses proposed files/commands from LLM output and executes them if authorized.
Includes safety guards (Path Traversal, Forbidden shell commands).
"""

import re
import os
import subprocess


def is_safe_path(path: str, workspace_root: str = "/project") -> bool:
    """Check if the target path resides safely within the workspace root."""
    try:
        abs_path = os.path.abspath(path)
        abs_workspace = os.path.abspath(workspace_root)
        # Handle symlink mapping checks if necessary
        return abs_path.startswith(abs_workspace)
    except Exception:
        return False


def is_safe_command(cmd: str) -> bool:
    """Verify that the shell command does not contain dangerous system actions."""
    # List of high-risk operational keywords
    blacklist = [
        "rm -rf /", "rm -rf  /", "rm -rf *", "rm -f *", "sudo", "su ",
        "chmod", "chown", "mkfs", "dd ", "shutdown", "reboot", "init 0",
        "rm -rf /project", "rm -rf doc", "rm -rf log"
    ]
    cmd_lower = cmd.lower().strip()
    for forbidden in blacklist:
        if forbidden in cmd_lower:
            return False
    return True


def parse_proposed_files(text: str) -> list[dict]:
    """Parse code blocks looking for files marked with '### FILE: <path>'."""
    pattern = re.compile(r"```[a-zA-Z0-9_\-#\+]*\n([\s\S]*?)```")
    blocks = pattern.findall(text)
    
    files = []
    for block in blocks:
        lines = block.split('\n')
        file_path = None
        content_start_idx = 0
        
        for i, line in enumerate(lines[:3]):
            # Support comments starting with # or //
            m = re.search(r"###\s*FILE:\s*([^\s\n]+)", line)
            if m:
                file_path = m.group(1).strip().replace("-->", "").strip()
                content_start_idx = i + 1
                break
                
        if file_path:
            file_content = "\n".join(lines[content_start_idx:])
            files.append({
                "path": file_path,
                "content": file_content
            })
    return files


def parse_proposed_commands(text: str) -> list[str]:
    """Parse bash code blocks marked with '### CMD:'."""
    pattern = re.compile(r"```[a-zA-Z0-9_\-#\+]*\n([\s\S]*?)```")
    blocks = pattern.findall(text)
    
    commands = []
    for block in blocks:
        lines = block.split('\n')
        has_cmd_tag = False
        content_start_idx = 0
        
        for i, line in enumerate(lines[:3]):
            if re.search(r"###\s*CMD:", line):
                has_cmd_tag = True
                content_start_idx = i + 1
                break
                
        if has_cmd_tag:
            cmd_text = "\n".join(lines[content_start_idx:]).strip()
            for c in cmd_text.split('\n'):
                c_clean = c.strip()
                # Skip blank lines and pure comments in command block
                if c_clean and not c_clean.startswith('#') and not c_clean.startswith('//'):
                    commands.append(c_clean)
    return commands


def apply_proposed_tools(answer: str, enabled_tools: list[str], workspace_root: str = "/project") -> str:
    """Parse and execute actions in the LLM answer if tools are authorized.

    Appends execution summary to the answer.
    """
    logs = []
    has_action = False

    # 1. Handle File Writing (edit)
    if "edit" in enabled_tools:
        proposed_files = parse_proposed_files(answer)
        if proposed_files:
            has_action = True
            logs.append("### ✏️ [Auto Edit] File Modification Results")
            for pf in proposed_files:
                target_path = pf["path"]
                # Resolve relative path if model supplied a simple relative path
                if not os.path.isabs(target_path):
                    target_path = os.path.join(workspace_root, target_path)
                
                # Security boundary check
                if not is_safe_path(target_path, workspace_root):
                    logs.append(f"- ❌ Blocked: Path '{pf['path']}' violates workspace bounds.")
                    continue
                
                try:
                    # Automatically create parent directories
                    os.makedirs(os.path.dirname(target_path), exist_ok=True)
                    # Write the content as UTF-8 (No BOM)
                    with open(target_path, "w", encoding="utf-8") as f:
                        f.write(pf["content"])
                    logs.append(f"- ✅ Applied: Successfully wrote/patched `{pf['path']}` ({len(pf['content'])} bytes)")
                except Exception as e:
                    logs.append(f"- ❌ Error writing `{pf['path']}`: {str(e)}")

    # 2. Handle Shell Execution (execute)
    if "execute" in enabled_tools:
        proposed_cmds = parse_proposed_commands(answer)
        if proposed_cmds:
            has_action = True
            logs.append("### 💻 [Auto Execute] Command Line Results")
            for cmd in proposed_cmds:
                # Security validation check
                if not is_safe_command(cmd):
                    logs.append(f"- ❌ Blocked: Command `{cmd}` rejected due to security filter.")
                    continue
                
                try:
                    # Run shell command under workspace root directory
                    res = subprocess.run(
                        cmd,
                        shell=True,
                        cwd=workspace_root,
                        capture_output=True,
                        text=True,
                        timeout=30 # Prevent hangs
                    )
                    if res.returncode == 0:
                        out = res.stdout.strip()
                        snippet = f"\n  ```text\n  {out[:300]}\n  ```" if out else " (No output)"
                        logs.append(f"- ✅ Run Successful: `{cmd}`{snippet}")
                    else:
                        err = res.stderr.strip()
                        logs.append(f"- ❌ Run Failed (code {res.returncode}): `{cmd}`\n  ```text\n  {err[:300]}\n  ```")
                except subprocess.TimeoutExpired:
                    logs.append(f"- ❌ Run Timeout: Command `{cmd}` expired after 30s.")
                except Exception as e:
                    logs.append(f"- ❌ Run Error on `{cmd}`: {str(e)}")

    if not has_action:
        return answer

    # Format the report and append it to LLM answer
    report_header = "\n\n---\n## ⚙️ OpenClaw Auto Execution Report\n"
    report_body = "\n".join(logs)
    
    return answer + report_header + report_body
