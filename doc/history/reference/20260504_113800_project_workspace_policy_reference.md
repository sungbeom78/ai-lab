# 작업 레퍼런스: desktop-ai Workspace 정책 구조화

- Date: 2026-05-04
- Project: project (workspace root)
- Area: Architecture & Policy
- Environment: WSL2 / desktop-ai
- Status: Completed
- Visibility:
  - [x] Internal
  - [ ] Publish Candidate
  - [ ] Published

## 1. 목적

`/project` 전체를 workspace root로 사용하는 환경에서,
경로별 수정 정책, 작업 모드, 권한 티어, 기록 정책을 문서화하고
재사용 가능한 workspace 구조를 구축한다.

## 2. 대상 환경

```text
OS: Ubuntu 24.04 (WSL2)
Host: Windows 11
Workspace Root: /project
심볼릭 링크: ai-hub → /mnt/d/project/ai-hub
             bomts-ai → /mnt/d/project/bomts-ai
             doc → /mnt/d/project/doc
             log → /mnt/d/project/log
             publish → /mnt/d/project/publish
             script → /mnt/d/project/script
             model → /home/<WSL_USER>/ai-local/model
             rag-index → /home/<WSL_USER>/ai-local/rag-index
             runtime → /home/<WSL_USER>/ai-local/runtime
             site → (NUC 마운트, 별도 mount 스크립트 필요)
             lostway → (NUC 마운트, 별도 mount 스크립트 필요)
```

## 3. 사전 조건

- `/project` 디렉토리 존재
- 각 심볼릭 링크가 올바른 대상에 연결
- ai-hub 기존 지침(프롬프트, 이력, 레퍼런스) 구조 완료

## 4. 작업 순서

### 4.1 현재 구조 확인

```bash
ls -la /project/
find /project -maxdepth 2 -type d 2>/dev/null | sort
```

### 4.2 README.md 생성

```bash
# /project/README.md 작성
# 포함: workspace 목적, 디렉토리 구조, 수정 정책, 작업 원칙
```

### 4.3 workspace.yaml 생성

```bash
# /project/workspace.yaml 작성
# 포함: workspace name, project list, modify_policy, git 전략, 민감 정보 정책
```

### 4.4 .gitignore 생성

```bash
# /project/.gitignore 작성
# 포함: model/, rag-index/, runtime/, log/, .venv/, node_modules/, .env
```

### 4.5 workspace_policy.md 생성

```bash
# /project/doc/workspace_policy.md 작성
# 포함: 경로별 역할/수정 범위, 작업 모드, 권한 티어, 기록 정책
```

### 4.6 git_strategy.md 생성

```bash
# /project/doc/git_strategy.md 작성
# 포함: 독립 repo + manifest 전략, submodule 장단점, 제외 디렉토리
```

## 5. 파일 구조

```text
/project/
├─ README.md              # workspace 개요
├─ workspace.yaml         # 프로젝트 매니페스트
├─ .gitignore            # git 제외 목록
└─ doc/
   ├─ workspace_policy.md # 전체 정책
   └─ git_strategy.md     # Git 전략
```

## 6. 검증 방법

```bash
# 파일 존재 확인
python - <<'PY'
from pathlib import Path
for path in [
    Path('/project/README.md'),
    Path('/project/workspace.yaml'),
    Path('/project/doc/workspace_policy.md'),
    Path('/project/doc/git_strategy.md'),
]:
    print(path, 'OK' if path.exists() and path.stat().st_size > 0 else 'EMPTY_OR_MISSING')
PY

# 민감 정보 검사
grep -RInE "api_key|apikey|token|secret|password|passwd|private_key|access_key" \
  /project/README.md /project/doc /project/workspace.yaml || true
```

## 7. 오류와 대응

| 증상 | 원인 | 대응 |
|------|------|------|
| site 경로 Permission denied | NUC 마운트 안 됨 | `bash /project/script/mount_site.sh` 실행 |
| lostway Permission denied | NUC 마운트 안 됨 | `bash /project/script/mount_lostway.sh` 실행 |
| workspace.yaml 파싱 오류 | YAML 문법 오류 | `python -c "import yaml; yaml.safe_load(open('/project/workspace.yaml'))"` |

## 8. 보안 주의사항

- 실제 IP, 계정명, 포트는 placeholder로 치환
- `.env` 파일은 git에서 제외
- workspace.yaml에 실제 비밀번호/토큰 미포함 확인

## 9. 재작업 체크리스트

* [x] 사전 조건 확인
* [x] 현재 구조 확인
* [x] README.md 생성
* [x] workspace.yaml 생성
* [x] .gitignore 생성
* [x] workspace_policy.md 생성
* [x] git_strategy.md 생성
* [x] 보안 정보 치환 확인

## 10. 관련 기록

```text
session:         /project/ai-hub/doc/history/session/20260504_113800_project_workspace_policy_session.md
ahnda log:       /project/ai-hub/doc/publish-source/ahnda/20260504_113800_project_workspace_policy_log.md
bomts publish:   /project/ai-hub/doc/publish-source/bomts/20260504_113800_project_workspace_policy_publish.md
```
