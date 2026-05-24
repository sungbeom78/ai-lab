# BomTS Technical Reference - OpenClaw Agentic Auto-Executor

본 문서는 OpenClaw Bridge Server의 단순 텍스트 챗 기능을 물리적 로컬 파일 패치 및 쉘 명령어 실행 에이전트로 승격시키기 위한 자동화 실행 엔진(`executor.py`)의 파싱 설계 및 보안 규격 명세서입니다.

---

## 1. 정규식 파서 및 추출 규격 (Parsing Specification)

마크다운 응답에서 파일 및 명령 정보를 추출하기 위해 두 가지 메타 주석 포맷 규격을 선언하고 백엔드 정규식 파서로 추출합니다.

### 1-1. Proposed Files 추출 (edit)
* **포맷**: 코드 블록의 상단 3라인 이내에 `### FILE: <file_absolute_path>` 형태의 주석 라인이 명시되어야 합니다.
* **추출 정규식**: `re.search(r"###\s*FILE:\s*([^\s\n]+)", line)`
* **작동 기전**:
  1. 마크다운의 ` ```javascript ... ``` ` 형태의 모든 코드 블록을 탐색합니다.
  2. 블록의 첫 3라인 중 `### FILE:` 주석이 감지되면 해당 문자열 뒤의 값을 절대경로로 파싱합니다.
  3. 경로 주석 메타 라인을 제외한 본문 코드 내용만 추출하여 대상 경로에 쓰기(Write)를 진행합니다.

### 1-2. Proposed Commands 추출 (execute)
* **포맷**: 코드 블록의 상단 3라인 이내에 `### CMD:` 주석 라인이 명시되어야 합니다.
* **추출 정규식**: `re.search(r"###\s*CMD:", line)`
* **작동 기전**:
  1. `### CMD:` 지시어가 탐색되면 주석 기호를 제외한 순수 명령어 라인들을 수집합니다.
  2. 빈 라인 및 단순 주석 라인은 배제하고 안전 검증을 수행한 뒤 쉘로 실행을 트리거합니다.

---

## 2. 보안 가이드 및 한계 경계선 (Security Guards)

로컬 시스템의 악의적인 행위 유발 및 경로 탈출을 원천 예방하기 위해 2중 안전 장치가 자동 구동됩니다.

### 2-1. 경로 이탈 방어 (Path Traversal Protection)
모든 쓰기 대상 파일의 주소는 반드시 지정된 워크스페이스 루트(예: `/project`)의 안쪽으로 절대경로가 해석되어야만 하며, `..` 등을 활용해 `/etc`나 중요 시스템 영역에 침투하려는 시도는 백엔드에서 사전 차단됩니다.
```python
def is_safe_path(path: str, workspace_root: str = "/project") -> bool:
    try:
        abs_path = os.path.abspath(path)
        abs_workspace = os.path.abspath(workspace_root)
        return abs_path.startswith(abs_workspace)
    except Exception:
        return False
```

### 2-2. 쉘 위험 키워드 필터링
터미널 명령어 실행(`subprocess.run`) 전에 시스템을 다운시키거나 무단 파괴할 우려가 높은 명령어 블랙리스트를 사전에 대조 필터링합니다.
* **차단 키워드**: `rm -rf /`, `rm -rf *`, `sudo`, `su `, `chmod`, `chown`, `mkfs`, `dd `, `shutdown`, `reboot` 등

---

## 3. API 실행 흐름 파이프라인
```text
[FastAPI Router /api/chat]
       │
       ▼ (1) Ollama 모델 응답 수령
[result["content"]]
       │
       ▼ (2) executor.apply_proposed_tools 호출
[executor.py (apply_proposed_tools)]
  ├── (3-1) edit 도구 체크 여부 및 '### FILE:' 파싱 -> os.makedirs 및 파일 쓰기 실행
  └── (3-2) execute 도구 체크 여부 및 '### CMD:' 파싱 -> subprocess.run 쉘 명령어 실행
       │
       ▼ (4) 실행 완료 상세 로그 요약 병합 (Auto Execution Report)
[final_answer] -> return
```
이 아키텍처적 구성을 통해 인텔리전트 가이드와 실질적 코딩 에이전틱이 완전한 결합을 이룹니다.
