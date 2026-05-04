import os
import json
from datetime import datetime
import re

OUT_DIR = "/project/ai-hub/out/local-ai-job"

def safe_filename(name):
    return re.sub(r'[^a-zA-Z0-9_\-]', '_', name)

def save_output(model: str, project: str, mode: str, task: str, response: str, metadata: dict):
    os.makedirs(OUT_DIR, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    model_safe = safe_filename(model)
    base_name = f"{timestamp}_{project}_{mode}_{model_safe}"
    
    md_path = os.path.join(OUT_DIR, f"{base_name}_result.md")
    json_path = os.path.join(OUT_DIR, f"{base_name}_metadata.json")
    
    # Save markdown
    with open(md_path, 'w', encoding='utf-8') as f:
        f.write(response)
        
    # Append output paths to metadata
    metadata["job_id"] = base_name
    metadata["output_file"] = md_path
    metadata["metadata_file"] = json_path
    
    # Save json
    with open(json_path, 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
        
    return md_path, json_path, metadata
