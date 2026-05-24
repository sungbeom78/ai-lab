"""OpenClaw Bridge Server - Main FastAPI Application.

Provides API endpoints for VS Code Extension:
- GET /api/health       - Health check with Ollama status
- POST /api/chat        - General chat with automatic model routing
- POST /api/instruction/run - Instruction file-based task execution
"""

from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

from . import ollama
from . import router as intent_router
from . import instruction
from . import session_logger
from app.local_ai_console import instruction_review
import os
from .config import CHAT_MODEL, CODE_MODEL

app = FastAPI(
    title="OpenClaw Bridge Server",
    description="Orchestrator between VS Code Extension and Ollama models",
    version="0.1.0",
)

# CORS: Allow VS Code Extension to connect
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ─── Request / Response Models ─────────────────────────────────────────────

class ChatRequest(BaseModel):
    workspaceRoot: str = "/project"
    message: str
    activeFile: str = ""
    selection: str = ""
    instructionPath: str = ""
    mode: str = "auto"  # auto | inspect | develop | etc.
    model: str = "auto" # auto | gemma3:4b | qwen2.5-coder:7b
    project: str = "ai-hub"
    temperature: float = 0.2
    usePipeline: bool = False
    tools: list[str] = []


class InstructionRunRequest(BaseModel):
    workspaceRoot: str = "/project"
    instructionPath: str
    message: str = ""
    mode: str = "auto"


# ─── Web & Health Check ────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
async def read_root():
    """Simple web interface to confirm the server is running."""
    html_content = f"""
    <!DOCTYPE html>
    <html lang="ko">
    <head>
        <meta charset="UTF-8">
        <title>OpenClaw Bridge Server</title>
        <style>
            body {{ font-family: sans-serif; padding: 40px; background: #f0f2f5; color: #333; }}
            .container {{ max-width: 600px; margin: 0 auto; background: #fff; padding: 30px; border-radius: 8px; box-shadow: 0 4px 6px rgba(0,0,0,0.1); }}
            h1 {{ color: #2c3e50; }}
            p {{ line-height: 1.6; }}
            .status {{ display: inline-block; padding: 5px 10px; background: #2ecc71; color: white; border-radius: 4px; font-weight: bold; }}
            .endpoint {{ background: #eee; padding: 10px; border-radius: 4px; font-family: monospace; overflow-x: auto; }}
        </style>
    </head>
    <body>
        <div class="container">
            <h1>🤖 OpenClaw Bridge Server</h1>
            <p>서버가 정상적으로 <span class="status">실행 중</span>입니다!</p>
            <p>이 서버는 VS Code 확장 프로그램(Extension)과 Ollama AI 간의 브릿지 역할을 수행하는 백엔드 API 서버입니다.</p>
            
            <h3>사용 가능한 엔드포인트:</h3>
            <div class="endpoint">
                <strong>GET</strong> /api/health<br>
                <strong>POST</strong> /api/chat<br>
                <strong>POST</strong> /api/instruction/run
            </div>
            
            <p style="margin-top: 20px; font-size: 0.9em; color: #666;">
                웹 채팅 UI가 필요하시다면 <strong><a href="http://127.0.0.1:11004" target="_blank" style="color: #3498db;">AI Hub (11004 포트)</a></strong>로 접속하여 OpenClaw 탭을 이용해 주세요.
            </p>
        </div>
    </body>
    </html>
    """
    return html_content


@app.get("/api/health")
async def health_check():
    """Health check endpoint. Verifies Ollama connectivity and model availability."""
    ollama_status = await ollama.check_health()
    chat_available = CHAT_MODEL in ollama_status.get("models", [])
    code_available = CODE_MODEL in ollama_status.get("models", [])

    return {
        "ok": ollama_status["ok"] and chat_available and code_available,
        "service": "openclaw-bridge",
        "version": "0.1.0",
        "ollama": ollama_status["ok"],
        "models": {
            "chat": CHAT_MODEL,
            "chat_available": chat_available,
            "code": CODE_MODEL,
            "code_available": code_available,
        },
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }


# ─── Chat Endpoint ────────────────────────────────────────────────────────


@app.post("/api/chat")
async def chat_endpoint(req: ChatRequest):
    """Chat endpoint. Routes to appropriate model based on message intent."""
    if not req.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")

    # 1. Classify intent and select model
    routing = await intent_router.classify_intent(req.message, req.mode)
    route = routing["route"]
    model = req.model if req.model != "auto" else routing["model"]

    # 2. Build context
    active_file_data = instruction.read_active_file(req.activeFile)
    active_file_content = active_file_data.get("content", "") if active_file_data.get("ok") else ""
    active_file_name = active_file_data.get("filename", "")

    # 3. Pipeline execution (if requested)
    pipeline_result = ""
    if getattr(req, "usePipeline", False):
        google_api_key = os.getenv("GOOGLE_API_KEY", "")
        reviewer_mode = "google-eval-required-later" if google_api_key else "local-only"
        
        # Run the official review pipeline that saves to out/instruction-review
        print(f"[Chat API] Running 3-Stage Pipeline (mode: {reviewer_mode})")
        review_metadata = instruction_review.run_review(
            title="VSCode Extension Request",
            target_project=req.project,
            request_type="VSCode Direct",
            draft_instruction=req.message,
            reviewer_mode=reviewer_mode,
            google_api_key=google_api_key
        )
        
        # Extract the final stage 3 output to override the instruction content
        v4_path = review_metadata["files"]["v4_stage3"]
        if os.path.isfile(v4_path):
            with open(v4_path, "r", encoding="utf-8") as f:
                pipeline_result = f.read()
        print(f"[Chat API] 3-Stage Pipeline completed. Review ID: {review_metadata['review_id']}")

    system_prompt = instruction.build_system_prompt(
        workspace_root=req.workspaceRoot,
        active_file_content=active_file_content,
        active_file_name=active_file_name,
        active_file_path=req.activeFile,
        selection=req.selection,
        tools=req.tools,
        mode=req.mode,
        target_project=req.project,
        temperature=req.temperature,
        instruction_content=pipeline_result  # pipeline result or empty
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": req.message},
    ]

    # 3. Call Ollama
    result = await ollama.chat(model=model, messages=messages, temperature=req.temperature)

    if not result["ok"]:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama error: {result.get('error', 'Unknown error')}",
        )

    # 4. Generate session ID and save log
    session_id = session_logger.generate_session_id()
    log_path = session_logger.save_session_log(
        workspace_root=req.workspaceRoot,
        session_id=session_id,
        user_message=req.message,
        instruction_path=req.instructionPath,
        active_file=req.activeFile,
        selection=req.selection,
        route=route,
        model=model,
        routing_reason=routing["reason"],
        answer=result["content"],
        mode=req.mode,
        target_project=req.project,
        temperature=req.temperature,
        enabled_tools=req.tools,
    )

    return {
        "ok": True,
        "model": model,
        "route": route,
        "answer": result["content"],
        "sessionId": session_id,
        "logPath": log_path,
        "routingReason": routing["reason"],
    }


# ─── Instruction Run Endpoint ─────────────────────────────────────────────


@app.post("/api/instruction/run")
async def instruction_run_endpoint(req: InstructionRunRequest):
    """Instruction-based task endpoint. Reads instruction file and generates plan."""
    # 1. Read instruction file
    instr_data = instruction.read_instruction_file(req.instructionPath)
    if not instr_data["ok"]:
        raise HTTPException(
            status_code=400,
            detail=f"Instruction file error: {instr_data.get('error', 'Unknown')}",
        )

    # 2. Classify intent
    combined_message = req.message or "이 지침을 분석하고 다음 작업을 판단해줘."
    routing = await intent_router.classify_intent(combined_message, req.mode)
    model = routing["model"]
    route = routing["route"]

    # 3. Build system prompt with instruction content
    system_prompt = instruction.build_system_prompt(
        workspace_root=req.workspaceRoot,
        instruction_content=instr_data["content"],
    )

    user_prompt = combined_message
    if req.message:
        user_prompt = req.message

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt},
    ]

    # 4. Call Ollama
    result = await ollama.chat(model=model, messages=messages)

    if not result["ok"]:
        raise HTTPException(
            status_code=502,
            detail=f"Ollama error: {result.get('error', 'Unknown error')}",
        )

    # 5. Save session log
    session_id = session_logger.generate_session_id()
    log_path = session_logger.save_session_log(
        workspace_root=req.workspaceRoot,
        session_id=session_id,
        user_message=combined_message,
        instruction_path=req.instructionPath,
        active_file="",
        selection="",
        route=route,
        model=model,
        routing_reason=routing["reason"],
        answer=result["content"],
        mode=req.mode,
    )

    return {
        "ok": True,
        "model": model,
        "route": route,
        "answer": result["content"],
        "sessionId": session_id,
        "logPath": log_path,
        "routingReason": routing["reason"],
        "instructionFile": instr_data["filename"],
    }
