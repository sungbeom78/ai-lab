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

## 현재 상태

| 레포 | git init | remote 등록 | 초기 commit | push |
|------|----------|------------|------------|------|
| on-premise-ai | ✅ | ✅ | ✅ | ❌ PAT 필요 |
| ai-lab | ✅ | ✅ | ❌ | ❌ |
| bomts-ai | ✅ | ✅ | ❌ | ❌ |
| lostway | ✅ | ✅ | ❌ | ❌ |
| site-ai | ✅ | ✅ | ❌ | ❌ |

## Pending: GitHub 인증 설정

### 방법 A: PAT (Personal Access Token) — 권장

1. GitHub → Settings → Developer settings → Personal access tokens → Fine-grained tokens
2. 권한: `Contents: Read and Write` (해당 repo 또는 all repos)
3. 토큰 복사 후:
   ```bash
   git -C /project push -u origin main
   # Username: sungbeom78
   # Password: <PAT 붙여넣기>
   ```
   (credential.helper=store 이므로 한 번만 입력하면 이후 자동 저장)

### 방법 B: SSH 키 GitHub 등록

1. 공개키 확인: `cat ~/.ssh/id_ed25519.pub`
2. GitHub → Settings → SSH and GPG keys → New SSH key 에 등록
3. Remote를 SSH로 변경:
   ```bash
   git -C /project remote set-url origin git@github.com:sungbeom78/on-premise-ai.git
   git -C /project/ai-hub remote set-url origin git@github.com:sungbeom78/ai-lab.git
   git -C /project/bomts-ai remote set-url origin git@github.com:sungbeom78/bomts-ai.git
   git -C /project/lostway remote set-url origin git@github.com:sungbeom78/lostway.git
   git -C /project/site remote set-url origin git@github.com:sungbeom78/site-ai.git
   ```

## 다음 작업 (인증 완료 후)

```bash
# 1. on-premise-ai push
cd /project && git push -u origin main

# 2. ai-lab 초기 commit & push
cd /project/ai-hub && git add . && git commit -m "Initial ai-lab setup" && git push -u origin main

# 3. site-ai 초기 commit & push
cd /project/site && git add . && git commit -m "Initial site-ai setup" && git push -u origin main

# 4. bomts-ai — push 전 민감 정보 확인 필수
cd /project/bomts-ai && git status  # 먼저 확인

# 5. lostway 초기 commit & push
cd /project/lostway && git add . && git commit -m "Initial lostway setup" && git push -u origin main
```
