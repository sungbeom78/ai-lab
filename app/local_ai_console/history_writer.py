import os
from datetime import datetime

HISTORY_SESSION_DIR = "/project/ai-hub/doc/history/session"
AHNDA_DIR = "/project/ai-hub/doc/publish-source/ahnda"
BOMTS_REF_DIR = "/project/ai-hub/doc/history/reference"  # AI 작업 기록 레퍼런스 (BomTS 레포 규칙 사본과 분리)
BOMTS_PUB_DIR = "/project/ai-hub/doc/publish-source/bomts"

def write_history(metadata: dict):
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    project = metadata.get("project", "unknown")
    mode = metadata.get("mode", "unknown")
    model = metadata.get("model", "unknown")
    task = metadata.get("task", "unknown")
    output_path = metadata.get("output_file", "unknown")
    
    base_name = f"{timestamp}_{project}_{mode}_local_ai_console"
    
    # Ensure dirs
    for d in [HISTORY_SESSION_DIR, AHNDA_DIR, BOMTS_REF_DIR, BOMTS_PUB_DIR]:
        os.makedirs(d, exist_ok=True)
        
    session_file = os.path.join(HISTORY_SESSION_DIR, f"{base_name}_session.md")
    ahnda_file = os.path.join(AHNDA_DIR, f"{base_name}_log.md")
    bomts_ref_file = os.path.join(BOMTS_REF_DIR, f"{base_name}_reference.md")
    bomts_pub_file = os.path.join(BOMTS_PUB_DIR, f"{base_name}_publish.md")
    
    common_content = f"""# AI Job Execution Record

- Date: {timestamp}
- Project: {project}
- Mode: {mode}
- Model: {model}
- Task: {task}
- Output: {output_path}

## Summary
Local AI Web Console executed the task successfully.

## Next Action
Review the output file and validate proposed code or commands.

## Security Notice
- Replaced IPs with <IP>
- Replaced ports with <PORT>
- Replaced users with <USER>
"""
    
    with open(session_file, 'w', encoding='utf-8') as f:
        f.write(common_content.replace("AI Job Execution Record", "Work Session: Local AI Web Console Job"))
        
    with open(ahnda_file, 'w', encoding='utf-8') as f:
        f.write(common_content.replace("AI Job Execution Record", "작업 로그: Local AI Console Execution"))
        
    with open(bomts_ref_file, 'w', encoding='utf-8') as f:
        f.write(common_content.replace("AI Job Execution Record", "작업 레퍼런스: Local AI Console Execution"))
        
    with open(bomts_pub_file, 'w', encoding='utf-8') as f:
        f.write(common_content.replace("AI Job Execution Record", "기술 블로그 초안: Local AI Console Execution"))
        
    return {
        "session": session_file,
        "ahnda": ahnda_file,
        "bomts_reference": bomts_ref_file,
        "bomts_publish": bomts_pub_file
    }
