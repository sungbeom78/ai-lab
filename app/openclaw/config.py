"""OpenClaw Bridge Server configuration."""

import os

# Server
OPENCLAW_HOST = os.getenv("OPENCLAW_HOST", "0.0.0.0")
OPENCLAW_PORT = int(os.getenv("OPENCLAW_PORT", "11005"))

# Ollama
OLLAMA_BASE_URL = os.getenv("OLLAMA_BASE_URL", "http://127.0.0.1:11434")

# Models
CHAT_MODEL = os.getenv("OPENCLAW_CHAT_MODEL", "gemma3:4b")
CODE_MODEL = os.getenv("OPENCLAW_CODE_MODEL", "qwen2.5-coder:7b")

# Workspace
DEFAULT_WORKSPACE_ROOT = os.getenv("OPENCLAW_WORKSPACE_ROOT", "/project")

# Cache paths (relative to workspace root)
CACHE_DIR = "cache/openclaw"
SESSION_DIR = f"{CACHE_DIR}/session"
INDEX_DIR = f"{CACHE_DIR}/index"
MEMORY_DIR = f"{CACHE_DIR}/memory"

# Routing keywords that trigger code model
CODE_KEYWORDS = [
    "코드 작성", "코드 수정", "리팩토링", "버그 수정", "테스트 작성",
    "API 구현", "파일 생성", "diff 생성", "patch 생성", "shell script",
    "TypeScript", "Python", "JavaScript", "Bash", "SQL",
    "에러 로그", "stacktrace", "error", "exception", "traceback",
    "코드", "code", "implement", "refactor", "debug", "fix",
    "function", "class", "module", "import", "export",
    "함수", "클래스", "모듈", "변수", "타입",
    "compile", "build", "lint", "test",
    "구현", "개발", "작성해", "만들어", "수정해", "고쳐",
]
