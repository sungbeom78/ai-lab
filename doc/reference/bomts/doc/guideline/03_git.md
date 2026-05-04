# 03. Git Ignore 및 디렉토리 구조 관리 지침

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)

---

## 1. 목적

Git 저장소에는 실행 결과물, 로그, 캐시, 민감정보를 포함하지 않고,
소스 코드와 구조만 관리한다.

---

## 2. 기본 원칙

* Git은 폴더가 아닌 파일을 기준으로 관리한다.
* 빈 폴더는 Git에 포함되지 않는다.
* 폴더 구조 유지를 위해 `.gitkeep` 파일을 사용한다.
* 실행 중 생성되는 모든 데이터는 Git에서 제외한다.

---

## 3. 디렉토리 관리 규칙

다음 디렉토리는 Git에서 제외한다.

* `log/`
* `data/`
* `tmp/`
* `cache/`

단, 디렉토리 구조 유지를 위해 `.gitkeep` 파일을 포함한다.

예시:

```
log/
└── .gitkeep

data/
└── .gitkeep
```

---

## 4. .gitignore 규칙

다음 규칙을 기본으로 사용한다.

```gitignore
# 로그 및 실행 결과
log/*
data/*
tmp/*
cache/*

# 디렉토리 유지용 파일은 포함
!log/.gitkeep
!data/.gitkeep
!tmp/.gitkeep
!cache/.gitkeep

# 환경 파일 및 민감 정보
.env
.env.*
*.env
!.env.example

# Config (운영 설정)
config/settings.yaml
config/cookies/
*.token
*.pid

# Python 캐시
__pycache__/
*.pyc

# 로그 파일
*.log

# 테스트 및 기타
.pytest_cache/
```

---

## 5. 민감 정보 관리

다음 정보는 절대 Git에 포함하지 않는다.

* API Key / Secret
* 계좌 정보
* 토큰 (access / refresh / cookie)
* DB 접속 정보
* 서버 IP / 포트 / 계정 조합
* 인증 파일 및 쿠키

모든 민감 정보는 `.env`에서만 관리한다.

---

## 6. 기존 파일 정리 규칙

이미 Git에 포함된 파일을 제외하려면 다음 명령어를 사용한다.

```bash
git rm -r --cached log/
git rm -r --cached data/
```

---

## 7. 신규 디렉토리 생성 규칙

새로운 디렉토리를 생성할 경우 다음을 반드시 수행한다.

1. `.gitkeep` 파일 생성
2. `.gitignore`에 해당 디렉토리 추가
3. 실행 결과물이 저장되는 경로인지 확인

---

## 8. Git 포함 / 제외 기준

**포함 (커밋 대상):**

| 항목 | 경로 |
|------|------|
| 소스 코드 | `src/` |
| 실행 진입점 | `run.py`, `run_test.py` |
| 테스트 라이브러리 | `lib_test/` |
| 지침 문서 | `doc/` |
| 참조 문서 | `references/` |
| 설정 예시 | `.env.example`, `settings.example.yaml` |
| 전략 흐름 | `config/trade/*.trade.yaml` |
| 스크립트 | `script/` |

**제외 (커밋 금지):**

| 항목 | 이유 |
|------|------|
| `.env` | 민감정보 |
| `config/settings.yaml` | 운영 파라미터 (서버별 상이) |
| `config/cookies/` | 인증 쿠키 |
| `*.token`, `*.pid` | 런타임 생성 파일 |
| `data/*` | 운영 데이터 (보관 기간 설정으로 자체 관리) |
| `log/*` | 로그 파일 |
| `tmp/*`, `cache/*` | 임시/캐시 파일 |
| `backup/`, `backups/` | 로컬 백업 |

---

## 9. 금지 사항

다음 행위를 금지한다.

* `.env` 파일을 Git에 커밋
* 로그/결과 파일 커밋
* 토큰/비밀번호 하드코딩
* 테스트 데이터 대량 업로드

---

## 10. 커밋 규칙

- 런타임 동작에 영향을 주는 변경 시 `doc/module_index.md`와 `doc/change_log.md` 반드시 업데이트.
- 문서 미업데이트 커밋은 불완전한 것으로 간주.
- `doc/change_log.md` 작성 형식 및 아카이브 규칙은 **GEMINI.md RULE 5** 준수.

---

## 11. 권장 사항

* Git commit 전 반드시 `git status` 확인
* `.gitignore` 변경 시 영향 범위 검토
* 디렉토리 구조는 명확하게 유지
* 실행 데이터와 소스 코드를 명확히 분리

---

## 12. 핵심 요약

* Git은 파일을 관리한다 (폴더 X)
* 빈 폴더는 `.gitkeep`으로 유지한다
* 실행 데이터는 모두 제외한다
* 민감 정보는 절대 포함하지 않는다
