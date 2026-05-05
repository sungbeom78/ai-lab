from fastapi import FastAPI, Request, Form, BackgroundTasks, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse, PlainTextResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from datetime import datetime
from typing import Optional
import os
import glob
import re

from . import ollama_client
from . import prompt_loader
from . import job_context
from . import output_writer
from . import history_writer
from . import safe_apply
from . import instruction_review as ir_module
from . import developer_request_writer as dr_writer

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


class InstructionReviewRequest(BaseModel):
    title: str
    target_project: str
    request_type: str
    draft_instruction: str
    reviewer_mode: str = "local-only"  # local-only | google-eval-required-later
    temperature: float = 0.2
    google_api_key: Optional[str] = None

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


# ─── Instruction Review Pipeline ───────────────────────────────────────────

IR_OUT_BASE = "/project/ai-hub/out/instruction-review"

@app.post("/api/instruction-reviews")
async def create_instruction_review(req: InstructionReviewRequest):
    try:
        metadata = ir_module.run_review(
            title=req.title,
            target_project=req.target_project,
            request_type=req.request_type,
            draft_instruction=req.draft_instruction,
            reviewer_mode=req.reviewer_mode,
            temperature=req.temperature,
            google_api_key=req.google_api_key,
        )
        review_id = metadata["review_id"]

        # Stage 3 결과 읽기
        v4_path = metadata["files"]["v4_stage3"]
        stage3_content = ""
        if os.path.isfile(v4_path):
            with open(v4_path, "r", encoding="utf-8") as f:
                stage3_content = f.read()

        # Developer Request 생성
        dr_result = dr_writer.write_developer_request(
            review_id=review_id,
            title=req.title,
            target_project=req.target_project,
            request_type=req.request_type,
            stage3_result=stage3_content,
            reviewer_mode=req.reviewer_mode,
        )

        return {
            "review_id": review_id,
            "status": "completed",
            "stage1_file": metadata["files"]["v2_stage1"],
            "stage2_file": metadata["files"]["v3_stage2"],
            "stage3_file": metadata["files"]["v4_stage3"],
            "developer_request_file": dr_result["doc_path"],
            "metadata_file": metadata["files"]["metadata"],
            "google_ai_used": metadata["google_ai_used"],
        }
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})


@app.get("/api/instruction-reviews")
async def list_instruction_reviews():
    if not os.path.exists(IR_OUT_BASE):
        return {"reviews": []}
    reviews = []
    for d in sorted(os.listdir(IR_OUT_BASE), reverse=True)[:20]:
        meta_path = os.path.join(IR_OUT_BASE, d, "review_metadata.json")
        if os.path.isfile(meta_path):
            try:
                import json
                with open(meta_path, "r", encoding="utf-8") as f:
                    meta = json.load(f)
                reviews.append({
                    "review_id": meta.get("review_id"),
                    "title": meta.get("title"),
                    "target_project": meta.get("target_project"),
                    "request_type": meta.get("request_type"),
                    "timestamp": meta.get("timestamp"),
                    "status": meta.get("status"),
                    "google_ai_used": meta.get("google_ai_used"),
                })
            except Exception:
                continue
    return {"reviews": reviews}


@app.get("/api/instruction-reviews/{review_id}")
async def get_instruction_review(review_id: str):
    if not re.match(r"^[a-zA-Z0-9_\-]+$", review_id):
        raise HTTPException(status_code=400, detail="Invalid review_id")
    meta_path = os.path.join(IR_OUT_BASE, review_id, "review_metadata.json")
    real_path = os.path.realpath(meta_path)
    real_base = os.path.realpath(IR_OUT_BASE)
    if not real_path.startswith(real_base):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not os.path.isfile(meta_path):
        raise HTTPException(status_code=404, detail="Review not found")
    import json
    with open(meta_path, "r", encoding="utf-8") as f:
        meta = json.load(f)
    # 각 Stage 결과 텍스트도 포함
    for key, fpath in meta.get("files", {}).items():
        if isinstance(fpath, str) and fpath.endswith(".md") and os.path.isfile(fpath):
            with open(fpath, "r", encoding="utf-8") as f:
                meta[f"{key}_content"] = f.read()
    return meta


# ─── Developer Requests ────────────────────────────────────────────────────

@app.get("/api/developer-requests")
async def list_developer_requests():
    items = dr_writer.list_developer_requests(limit=20)
    return {"requests": items}


@app.get("/api/developer-requests/{request_id}")
async def get_developer_request(request_id: str):
    item = dr_writer.get_developer_request(request_id)
    if item is None:
        raise HTTPException(status_code=404, detail="Developer request not found")
    return item

# ─── OpenClaw Configuration ────────────────────────────────────────────────

@app.get("/api/openclaw/config")
async def get_openclaw_config():
    return {
        "web_url": os.getenv("OPENCLAW_WEB_URL", "http://127.0.0.1:11006"),
        "api_url": os.getenv("OPENCLAW_API_URL", "http://127.0.0.1:11006")
    }

