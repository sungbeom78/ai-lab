---
description: Auto-approval policy for terminal commands (3-tier classification)
---

# 명령어 자동 승인 정책

> A등급(무조건 자동 승인) 명령어는 별도 파일에서 관리한다:
> → `/safe-command-policy-SafeToAutoRun` 참조

## Turbo 어노테이션 정의

| 어노테이션 | 위치 | 의미 |
|-----------|------|------|
| `// turbo` | 특정 단계 **위** | 해당 단계만 자동 승인 + 중단 없이 실행 |
| `// turbo-all` | 파일 **어디든** | 해당 워크플로우 내 모든 `run_command` 호출을 자동 승인 + 중단 없이 연속 실행 |

## 관련 워크플로우
- A등급 자동 승인 명령어 → /safe-command-policy-SafeToAutoRun
- 파일 수정 절차 내 명령어 → /edit-file-procedure
- 코드 변경 검증 명령어 → /change-code-procedure

---

## B등급: 조건부 자동 승인 (SafeToAutoRun = true, 단 조건 충족 시)

| 명령어 | 자동 승인 조건 |
|--------|--------------|
| `python run_test.py qa_quick` | 항상 가능 |
| `python run_test.py qa_standard` | 항상 가능 |
| `python run_test.py qa_full` | 항상 가능 |
| `python tmp/test_*.py` | 프로젝트 내부 tmp/ 대상 테스트 스크립트 실행 |
| `pytest lib_test/<특정파일>` | 파일명이 명시된 경우만 |
| `Get-Content -Tail N <logs/*>` | 대상이 logs/ 하위인 경우만 |
| `python -c "... requests.get('http://localhost:...')"` | localhost 대상 GET만 (아래 환경 범위 참조) |
| `New-Item -ItemType Directory tmp/backup/config/<timestamp>` | 설정 파일 수정 절차(/edit-file-procedure) 내부에서만 |

### localhost 환경 범위
- 허용: `127.0.0.1`, `localhost` (WSL ↔ Windows 간 통신 포함)
- 금지: 외부 IP 주소, 외부 도메인 — C등급 적용

> **워크플로우 내부 예외 원칙**: 워크플로우 절차 안에서 명시적으로 사용되는 명령어는
> C등급에 해당하더라도 해당 절차 수행 중에 한하여 B등급으로 승격된다.

---

## C등급: 자동 승인 금지 (SafeToAutoRun = false, 반드시 사용자 승인)

| 범주 | 예시 |
|------|------|
| 서비스 시작/중지 | `python run.py --start`, `python run.py --stop` |
| DB 변경 | INSERT, UPDATE, DELETE, DROP |
| 파일 삭제/이동 | `Remove-Item`, `Move-Item`, `del` |
| 파일 생성 | `New-Item`, `mkdir` — 단, 워크플로우 내부 예외 제외 (위 B등급 참조) |
| 패키지 설치 | `pip install`, `npm install` |
| Git 쓰기 | `git commit`, `git push`, `git merge` |
| 외부 네트워크 호출 | localhost 외 대상 HTTP 요청 |
| 와일드카드 테스트 | `pytest lib_test/` (전체), `python run_test.py *` |
| 설정 파일 직접 수정 | PowerShell로 .env/yaml 직접 쓰기 |
