from datetime import datetime

def create_prompt(model: str, project: str, mode: str, task: str, prompt_data: dict):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    full_prompt = f"""You are an AI executing a task on the Local AI Console.

[Context Info]
- Model: {model}
- Project: {project}
- Mode: {mode}
- Current Time: {current_time}

[System Prompt]
{prompt_data['system_prompt']}

[Project Prompt]
{prompt_data['project_prompt']}

[Task]
{prompt_data['task_prompt']}

[Output Requirements]
모든 응답은 한국어로 작성한다. (All responses must be written in Korean)

Please provide your output exactly in the following format:

# Local AI Job Result

## 1. Summary

## 2. Assumptions

## 3. Plan

## 4. Proposed Files

## 5. Proposed Commands

## 6. Validation

## 7. Risks

## 8. Next Action

## 9. Ahnda Log Draft

## 10. BomTS Reference Draft
"""
    return full_prompt
