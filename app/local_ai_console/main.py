from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
import os
import glob

from . import ollama_client
from . import prompt_loader
from . import job_context
from . import output_writer
from . import history_writer
from . import safe_apply

app = FastAPI(title="Local AI Web Console")
app.include_router(safe_apply.router, prefix="/api")

# Setup static and templates
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
app.mount("/static", StaticFiles(directory=os.path.join(BASE_DIR, "static")), name="static")
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

class JobRequest(BaseModel):
    model: str
    project: str
    mode: str
    task: str
    temperature: float = 0.2
    dry_run: bool = False

@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request):
    return templates.TemplateResponse(request=request, name="index.html")

@app.get("/api/health")
async def health_check():
    return {
        "status": "ok",
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    }

@app.get("/api/models")
async def get_models():
    models = ollama_client.get_models()
    if isinstance(models, dict) and "error" in models:
        return JSONResponse(status_code=500, content=models)
    return {"models": models}

@app.post("/api/jobs")
async def create_job(job_req: JobRequest):
    try:
        # Load prompt
        prompt_data = prompt_loader.load_prompt(job_req.project, job_req.task)
        
        # Build context
        full_prompt = job_context.create_prompt(
            job_req.model, job_req.project, job_req.mode, job_req.task, prompt_data
        )
        
        metadata = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "model": job_req.model,
            "project": job_req.project,
            "mode": job_req.mode,
            "task": job_req.task,
            "dry_run": job_req.dry_run,
            "temperature": job_req.temperature,
            "prompt_files_used": prompt_data["prompts_used"],
            "missing_prompt_files": prompt_data["missing_prompts"],
            "status": "success"
        }
        
        if job_req.dry_run:
            response_text = f"# Dry Run Mode\n\n## Generated Prompt\n```\n{full_prompt}\n```"
        else:
            response_text = ollama_client.generate(job_req.model, full_prompt, job_req.temperature)
            if response_text.startswith("Error"):
                metadata["status"] = "error"
                metadata["error_message"] = response_text
                
        # Save output
        md_path, json_path, metadata = output_writer.save_output(
            job_req.model, job_req.project, job_req.mode, job_req.task, response_text, metadata
        )
        
        # Save history
        history_paths = history_writer.write_history(metadata)
        
        return {
            "output_file": md_path,
            "metadata_file": json_path,
            "history_files": history_paths,
            "response": response_text,
            "status": metadata["status"]
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/api/jobs")
async def get_jobs():
    out_dir = "/project/ai-hub/out/local-ai-job"
    if not os.path.exists(out_dir):
        return {"jobs": []}
    
    files = glob.glob(os.path.join(out_dir, "*_result.md"))
    files.sort(key=os.path.getmtime, reverse=True)
    
    jobs = []
    for f in files[:10]:
        base_name = os.path.basename(f).replace("_result.md", "")
        jobs.append({
            "name": os.path.basename(f),
            "job_id": base_name,
            "path": f
        })
    return {"jobs": jobs}

@app.get("/api/jobs/{job_id}/result", response_class=PlainTextResponse)
async def get_job_result(job_id: str):
    import re
    if not re.match(r"^[a-zA-Z0-9_\-]+$", job_id):
        raise HTTPException(status_code=400, detail="Invalid job_id")
        
    out_dir = "/project/ai-hub/out/local-ai-job"
    file_path = os.path.join(out_dir, f"{job_id}_result.md")
    
    if not os.path.isfile(file_path):
        raise HTTPException(status_code=404, detail="Result file not found")
        
    with open(file_path, "r", encoding="utf-8") as f:
        return f.read()
