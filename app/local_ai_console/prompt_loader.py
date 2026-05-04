import os

PROMPT_BASE_DIR = "/project/ai-hub/prompt"

def load_prompt(project: str, task: str):
    prompts_used = []
    missing_prompts = []
    
    system_prompt_path = os.path.join(PROMPT_BASE_DIR, "system", "ai_hub_work_start.md")
    project_prompt_path = os.path.join(PROMPT_BASE_DIR, "project", f"{project}_work_start.md")
    
    system_prompt = ""
    if os.path.exists(system_prompt_path):
        with open(system_prompt_path, 'r', encoding='utf-8') as f:
            system_prompt = f.read()
        prompts_used.append(system_prompt_path)
    else:
        missing_prompts.append(system_prompt_path)
        
    project_prompt = ""
    if project and os.path.exists(project_prompt_path):
        with open(project_prompt_path, 'r', encoding='utf-8') as f:
            project_prompt = f.read()
        prompts_used.append(project_prompt_path)
    elif project:
        missing_prompts.append(project_prompt_path)
        
    return {
        "system_prompt": system_prompt,
        "project_prompt": project_prompt,
        "task_prompt": task,
        "prompts_used": prompts_used,
        "missing_prompts": missing_prompts
    }
