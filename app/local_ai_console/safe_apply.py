import os
import json
import re
from datetime import datetime
from fastapi import APIRouter, HTTPException

router = APIRouter()

AHNDA_BASE_DIR = "/project/site/ahnda"

ALLOWED_FILES = [
    "index.html",
    "assets/css/style.css",
    "assets/js/app.js",
    "data/schedule.json",
    "data/work_log.json",
    "data/memo.json",
    "data/study.json"
]

def check_sensitive_content(content: str):
    sensitive_patterns = [
        "api_key", "apikey", "token", "secret", "password", "passwd",
        r"https?://"
    ]
    for pattern in sensitive_patterns:
        if re.search(pattern, content, re.IGNORECASE):
            return f"Blocked by rule: contains sensitive or external URL pattern '{pattern}'"
    return None

def get_ahnda_mvp_files():
    files = {}

    files["index.html"] = """<!DOCTYPE html>
<html lang="ko">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Ahnda 개인 작업실</title>
    <link rel="stylesheet" href="assets/css/style.css">
</head>
<body>
    <div class="container">
        <header>
            <h1>오늘의 대시보드</h1>
            <p>Ahnda MVP - 내 작업과 일정을 관리합니다.</p>
        </header>

        <main class="grid-layout">
            <section class="card" id="schedule-section">
                <h2>일정</h2>
                <div id="schedule-content">로딩 중...</div>
            </section>
            
            <section class="card" id="worklog-section">
                <h2>작업 로그</h2>
                <div id="worklog-content">로딩 중...</div>
            </section>
            
            <section class="card" id="memo-section">
                <h2>메모</h2>
                <div id="memo-content">로딩 중...</div>
            </section>
            
            <section class="card" id="study-section">
                <h2>스터디 기록</h2>
                <div id="study-content">로딩 중...</div>
            </section>
        </main>
    </div>
    <script src="assets/js/app.js"></script>
</body>
</html>
"""

    files["assets/css/style.css"] = """* {
    box-sizing: border-box;
    margin: 0;
    padding: 0;
}

body {
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #121212;
    color: #e0e0e0;
    line-height: 1.6;
}

.container {
    max-width: 1200px;
    margin: 0 auto;
    padding: 20px;
}

header {
    margin-bottom: 30px;
    border-bottom: 1px solid #333;
    padding-bottom: 20px;
}

header h1 {
    color: #ffffff;
    font-size: 2rem;
    margin-bottom: 10px;
}

header p {
    color: #aaaaaa;
}

.grid-layout {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
    gap: 20px;
}

.card {
    background-color: #1e1e1e;
    border-radius: 8px;
    padding: 20px;
    box-shadow: 0 4px 6px rgba(0, 0, 0, 0.3);
    border: 1px solid #2a2a2a;
}

.card h2 {
    color: #ffffff;
    font-size: 1.2rem;
    margin-bottom: 15px;
    border-bottom: 1px solid #333;
    padding-bottom: 10px;
}

.item {
    margin-bottom: 15px;
    padding-bottom: 15px;
    border-bottom: 1px dashed #333;
}
.item:last-child {
    margin-bottom: 0;
    padding-bottom: 0;
    border-bottom: none;
}

.item-title {
    font-weight: bold;
    color: #64b5f6;
    margin-bottom: 5px;
}

.item-desc {
    color: #cccccc;
    font-size: 0.9rem;
}
"""

    files["assets/js/app.js"] = """document.addEventListener('DOMContentLoaded', () => {
    loadData('schedule', 'data/schedule.json', renderSchedule);
    loadData('worklog', 'data/work_log.json', renderWorkLog);
    loadData('memo', 'data/memo.json', renderMemo);
    loadData('study', 'data/study.json', renderStudy);
});

function escapeHtml(unsafe) {
    if (!unsafe) return '';
    return unsafe
         .toString()
         .replace(/&/g, "&amp;")
         .replace(/</g, "&lt;")
         .replace(/>/g, "&gt;")
         .replace(/"/g, "&quot;")
         .replace(/'/g, "&#039;");
}

async function loadData(id, url, renderFn) {
    const el = document.getElementById(id + '-content');
    try {
        const res = await fetch(url);
        if (!res.ok) throw new Error('Network response was not ok');
        const data = await res.json();
        el.innerHTML = renderFn(data);
    } catch (e) {
        el.innerHTML = `<p style="color: #ff5252;">데이터를 불러오는 중 오류가 발생했습니다.</p>`;
    }
}

function renderSchedule(data) {
    if (!data || data.length === 0) return '<p>일정이 없습니다.</p>';
    return data.map(item => `
        <div class="item">
            <div class="item-title">${escapeHtml(item.time)} - ${escapeHtml(item.title)}</div>
            <div class="item-desc">${escapeHtml(item.description)}</div>
        </div>
    `).join('');
}

function renderWorkLog(data) {
    if (!data || data.length === 0) return '<p>작업 로그가 없습니다.</p>';
    return data.map(item => `
        <div class="item">
            <div class="item-title">${escapeHtml(item.date)} - ${escapeHtml(item.project)}</div>
            <div class="item-desc">${escapeHtml(item.task)}</div>
        </div>
    `).join('');
}

function renderMemo(data) {
    if (!data || data.length === 0) return '<p>메모가 없습니다.</p>';
    return data.map(item => `
        <div class="item">
            <div class="item-title">${escapeHtml(item.title)}</div>
            <div class="item-desc">${escapeHtml(item.content)}</div>
        </div>
    `).join('');
}

function renderStudy(data) {
    if (!data || data.length === 0) return '<p>스터디 기록이 없습니다.</p>';
    return data.map(item => `
        <div class="item">
            <div class="item-title">${escapeHtml(item.topic)}</div>
            <div class="item-desc">${escapeHtml(item.summary)}</div>
        </div>
    `).join('');
}
"""

    files["data/schedule.json"] = """[
    {"time": "09:00", "title": "일일 점검", "description": "전일 작업 내역 확인 및 금일 목표 설정"},
    {"time": "14:00", "title": "개발 세션", "description": "Ahnda MVP 정적 웹 개발"}
]"""

    files["data/work_log.json"] = """[
    {"date": "2026-05-03", "project": "ahnda", "task": "다크톤 카드형 UI 프로토타입 작성"}
]"""

    files["data/memo.json"] = """[
    {"title": "개발 아이디어", "content": "Local AI Console에서 직접 적용 가능하도록 Safe Apply 기능 구현"}
]"""

    files["data/study.json"] = """[
    {"topic": "FastAPI", "summary": "APIRouter를 활용한 모듈 분리 방법 학습"}
]"""

    return files

@router.get("/apply/site-ahnda-static-mvp/preview")
async def preview_apply_ahnda_mvp():
    files_to_write = get_ahnda_mvp_files()
    preview = []
    
    for rel_path, content in files_to_write.items():
        if rel_path not in ALLOWED_FILES:
            continue
            
        full_path = os.path.join(AHNDA_BASE_DIR, rel_path)
        action = "Create"
        if os.path.exists(full_path):
            action = "Update (will backup existing)"
            
        err = check_sensitive_content(content)
        if err:
            action = f"Blocked: {err}"
            
        preview.append({
            "path": rel_path,
            "action": action,
            "size": len(content)
        })
        
    return {"preview": preview}

@router.post("/apply/site-ahnda-static-mvp")
async def apply_ahnda_mvp():
    files_to_write = get_ahnda_mvp_files()
    results = []
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    for rel_path, content in files_to_write.items():
        if rel_path not in ALLOWED_FILES:
            continue
            
        full_path = os.path.join(AHNDA_BASE_DIR, rel_path)
        
        # Path traversal check
        if not os.path.abspath(full_path).startswith(os.path.abspath(AHNDA_BASE_DIR)):
            results.append({"path": rel_path, "status": "failed", "error": "Path traversal blocked"})
            continue
            
        err = check_sensitive_content(content)
        if err:
            results.append({"path": rel_path, "status": "failed", "error": err})
            continue
            
        try:
            os.makedirs(os.path.dirname(full_path), exist_ok=True)
            
            # Backup if exists
            if os.path.exists(full_path):
                bak_path = f"{full_path}.bak_{timestamp}"
                os.rename(full_path, bak_path)
                results.append({"path": rel_path, "status": "backed_up", "backup": bak_path})
                
            with open(full_path, "w", encoding="utf-8") as f:
                f.write(content)
                
            results.append({"path": rel_path, "status": "success"})
        except Exception as e:
            results.append({"path": rel_path, "status": "error", "error": str(e)})
            
    return {"status": "completed", "results": results}
