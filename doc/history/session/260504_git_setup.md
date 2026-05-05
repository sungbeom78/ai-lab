# Session Log: Git 레포지토리 초기 설정

- Date: 2026-05-04T23:44 KST
- Plan Reference: `/project/doc/plan/260504_git_start.md`

## 목표

`/project` 워크스페이스의 5개 git 레포지토리를 초기화하고 GitHub remote를 연결한다.

| 경로 | repo 이름 | visibility |
|------|-----------|------------|
| `/project` | `on-premise-ai` | private |
| `/project/ai-hub` | `ai-lab` | public |
| `/project/bomts-ai` | `bomts-ai` | private |
| `/project/lostway` | `lostway` | public |
| `/project/site` | `site-ai` | private |

## 주요 발견사항

- `/project` 하위 일부 디렉토리는 `/mnt/d/project/...` 로의 **심볼릭 링크**
  - 심볼릭 링크: `ai-hub`, `bomts-ai`, `doc`, `script`, `publish`, `log`
  - 실제 디렉토리: `lostway`, `site`
- git은 심볼릭 링크 내부를 직접 add할 수 없음 → 링크 자체를 add
- `lostway/`, `site/`는 실제 디렉토리이자 독립 git repo → nested repo 충돌 없이 `.gitignore`로 제외

## 실행 내용

### 1. 스크립트 생성

- 파일: `/project/script/setup_git_repos.sh`
- 심볼릭 링크 대응을 위해 `real_path()` 함수 추가 (원본 계획 스크립트 보완)
- `.gitignore` 기존 파일 존재 시 `append_if_missing`으로 패턴 추가 (덮어쓰기 안 함)

### 2. 스크립트 실행

```
bash /project/script/setup_git_repos.sh
```

**결과:**
- 5개 레포 모두 `git init` 및 `origin` remote 등록 성공
- `.gitignore` 생성/보완 완료
- `.gitkeep` placeholder 생성 완료

### 3. git global 설정

```bash
git config --global init.defaultBranch main
git config --global user.name "sungbeom78"
git config --global user.email "sungbeom78@users.noreply.github.com"
git config --global credential.helper store
```

### 4. on-premise-ai 초기 commit

```bash
cd /project
git add .gitignore README.md workspace.yaml ai-hub bomts-ai doc publish script
git commit -m "Initial workspace setup"
```

**Commit:** `e7930af`  
**포함 파일:** .gitignore, README.md, workspace.yaml, ai-hub(symlink), bomts-ai(symlink), doc(symlink), publish(symlink), script(symlink)

### 5. push 시도 결과

HTTPS push 시 credential 대기 중으로 중단됨.

**원인:**
- SSH 키(`id_ed25519`)는 존재하나 GitHub에 등록되어 있지 않거나 SSH remote가 아님
- HTTPS remote 사용 중 → GitHub PAT 필요

**설정 완료:**
- `credential.helper = store` 설정 완료

## 최종 상태 (2026-05-05)

| 레포 | git init | remote 등록 | 초기 commit | push | 비고 |
|------|----------|------------|------------|------|------|
| on-premise-ai | ✅ | ✅ | ✅ `e7930af` | ✅ | .gitignore 추가 commit `54ff7db` |
| ai-lab | ✅ | ✅ | ✅ `efb23df` | ✅ | |
| bomts-ai | ✅ | ✅ | ✅ `4b236f3` | ✅ | .gitignore + .gitkeep only (안전) |
| lostway | ✅ | ✅ | ✅ `0376aa1` | ✅ | .gitignore + .gitkeep only |
| site-ai | ✅ | ✅ | ✅ `1d477d2` | ✅ | server.log/pid 제거 `871be51` |

## 완료

모든 레포 초기 push 완료. credential.helper=store 설정으로 이후 push는 자동 인증.
