# 11. Glossary Submodule Integration Guide

> Glossary 서브모듈을 메인 시스템에서 강제하고, 타 프로젝트에도 적용하기 위한 관리 가이드.

---

## 1. 개요

Glossary 서브모듈은 **단어 수준의 식별자 관리 시스템**이다.
모든 프로젝트에서 동일한 용어 사전을 공유함으로써:

- 프로젝트 간 식별자 일관성 확보
- AI 에이전트의 임의 명명 방지
- 코드 네비게이션 및 의사소통 품질 향상

---

## 2. 서브모듈 구조

```
glossary/                          # Git submodule (독립 저장소)
├── dictionary/                    # Source of Truth
│   ├── words.json                 # 단어 사전 (root)
│   ├── compounds.json             # 복합어 사전
│   ├── banned.json                # 금지어
│   ├── pending_words.json         # 보류 단어
│   ├── drafts.json                # 보류(스캔 후보)
│   └── tech_abbreviations.json   # 기술 약어 (coro, ymd 등)
├── build/index/                   # 자동 생성 인덱스
│   ├── word_min.json
│   ├── compound_min.json
│   └── variant_map.json
├── core/                          # 검증/감사 엔진
│   ├── auditor.py                 # 식별자 감사기
│   ├── writer.py                  # 사전 수정기 (유일한 쓰기 경로)
│   └── token_rules.py            # 토큰 분류/필터
├── bin/                           # CLI 도구
│   ├── scan_items.py              # 소스 코드 미등록 식별자 스캔
│   ├── batch_items.py             # AI 배치 분석
│   └── run.py                     # validate + generate 원샷
├── web/                           # 관리 UI
│   ├── server.py                  # Flask 웹 서버
│   └── index.html                 # 대시보드 UI
├── .scan_list                     # 스캔 대상 폴더/파일
├── .scan_ignore                   # 스캔 제외 패턴
├── generate_glossary.py           # 인덱스 생성/검증 CLI
└── README.md                      # 서브모듈 문서
```

---

## 3. 신규 프로젝트에 적용하기

### 3-1. 서브모듈 추가

```bash
# 프로젝트 루트에서 실행
git submodule add <glossary-repo-url> glossary
git submodule update --init --recursive
```

### 3-2. 스캔 대상 설정

프로젝트 구조에 맞게 `glossary/.scan_list`를 수정한다:

```
# .scan_list
dir:src               # ← 소스 코드 디렉토리
dir:config             # ← 설정 파일
root:run*.py           # ← 루트 진입점
```

### 3-3. 스캔 제외 설정

외부 종속성, 생성물, 테스트 등은 `glossary/.scan_ignore`에서 제외한다:

```
# .scan_ignore
**/node_modules/**
**/venv/**
**/__pycache__/**
**/build/**
**/dist/**
```

### 3-4. 인덱스 생성

```bash
python glossary/generate_glossary.py generate
```

> 이 명령은 `words.json` + `compounds.json` → `build/index/` 파일을 생성한다.
> 인덱스가 없으면 auditor/scanner가 동작하지 않는다.

---

## 4. AI 에이전트 연동 (자동 강제)

### 4-1. AGENTS.md에 추가할 규칙

타 프로젝트의 `AGENTS.md`에 아래 규칙을 추가하여 AI 에이전트에게 용어 사전 준수를 강제한다:

```markdown
## GLOSSARY COMPLIANCE (MANDATORY)

### Rule G-0: 기존 등록 용어 우선 사용

새 식별자를 만들기 전에, 동일/유사 의미의 단어가 이미 등록되어 있는지
**동의어 교차 검색**을 반드시 수행한다.

절차:
1. 표현하려는 의미를 정의한다.
2. 그 의미의 **영어 동의어를 최소 3개** 나열한다.
3. 각 동의어를 `glossary/dictionary/words.json`에서 조회한다.
4. 등록된 단어가 있으면 → **반드시 그 단어를 사용한다.**
5. 어느 것도 없으면 → 가장 일반적 형태를 선택하여 신규 등록 절차 진행.

### Rule G-1: 미등록 단어 사용 금지

식별자에 필요한 단어가 용어 사전에 없으면:
1. `python glossary/generate_glossary.py check-id <식별자>` 실행
2. 미등록 단어 발견 시 → 개발 중단, 사용자 승인 요청
3. 승인 후에만 식별자 생성 가능

### 감사 도구

| 도구 | 용도 |
|------|------|
| `python glossary/generate_glossary.py check-id <id>` | 식별자 검증 |
| `python glossary/generate_glossary.py validate` | 전체 사전 무결성 |
| `python glossary/generate_glossary.py generate` | 인덱스 재생성 |
| `python glossary/bin/scan_items.py --mode word --json` | 코드 스캔 |
```

### 4-2. 워크플로우 파일 복사

`.agents/workflows/new-identifier-procedure.md`를 타 프로젝트에도 복사한다:

```bash
# 타 프로젝트 루트에서
mkdir -p .agents/workflows
cp glossary/.agents/workflows/new-identifier-procedure.md .agents/workflows/
```

> 또는 glossary 서브모듈 내 `.agents/` 경로를 직접 참조하도록
> `AGENTS.md`에 `Applicable workflows`에 추가:
> ```markdown
> - `glossary/.agents/workflows/new-identifier-procedure.md`
> ```

---

## 5. CI/CD 연동  (선택)

### 5-1. 사전 검증 스크립트

```bash
#!/bin/bash
# ci/check_glossary.sh — PR 검증용

set -e

echo "=== Glossary Index Generation ==="
python glossary/generate_glossary.py generate

echo "=== Glossary Validation ==="
python glossary/generate_glossary.py validate

echo "=== Identifier Scan ==="
RESULT=$(python glossary/bin/scan_items.py --mode word --json 2>/dev/null)
COUNT=$(echo "$RESULT" | python -c "import sys,json; print(json.load(sys.stdin)['count'])")

if [ "$COUNT" -gt 0 ]; then
    echo "FAIL: $COUNT unregistered words found"
    echo "$RESULT" | python -c "
import sys,json
d=json.load(sys.stdin)
for c in d['candidates']:
    print(f\"  {c['name']:20s}  {','.join(c['sources'][:2])}\")
"
    exit 1
fi

echo "PASS: All identifiers registered"
```

### 5-2. GitHub Actions 예시

```yaml
# .github/workflows/glossary-check.yml
name: Glossary Check
on: [pull_request]
jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
        with:
          submodules: recursive
      - uses: actions/setup-python@v5
        with:
          python-version: '3.10'
      - run: pip install httpx
      - run: bash ci/check_glossary.sh
```

---

## 6. 명명 규칙 빠른 참조

### 6-1. 동의어 교차 검색 (G-0 준수)

새 식별자 결정 시 반드시 수행:

```
의미 정의 → 동의어 3개 이상 나열 → 각각 사전 조회 → 등록된 것 사용
```

예시:

| 의미 | 동의어 후보 | 사전 조회 결과 | 선택 |
|------|------------|---------------|------|
| 취소 | cancel, abort, revoke | `cancel` ✅ 등록됨 | cancel |
| 조회 | get, fetch, retrieve | `get` ✅ 등록됨 | get |
| 전송 | send, transmit, dispatch | `send` ✅ 등록됨 | send |
| 시작 | start, begin, launch, init | `start` ✅ 등록됨 | start |
| 생성 | create, make, build, generate | `create` ✅ 등록됨 | create |

### 6-2. 단수/복수 원칙

| 위치 | 규칙 | 예시 |
|------|------|------|
| 폴더명 | **반드시 단수** | `log/`, `script/`, `test/` |
| 테이블명 | **반드시 단수** | `order`, `position` |
| 변수 (단일) | 단수 | `order = Order()` |
| 변수 (컬렉션) | 복수 | `orders = list[Order]` |

### 6-3. 기본 형태(base form) 사용

| 원래 | 기본 형태 | 사유 |
|------|----------|------|
| cancelling | cancel | 동사 원형 |
| retrieved | retrieve | 동사 원형 |
| states | state | 단수형 |
| running | run | 동사 원형 |

---

## 7. 용어 사전 공유 전략

### 7-1. 단일 저장소 (권장)

모든 프로젝트가 **동일한 glossary 서브모듈 저장소**를 참조한다:

```
project-a/glossary → git submodule → glossary-repo (main)
project-b/glossary → git submodule → glossary-repo (main)
project-c/glossary → git submodule → glossary-repo (main)
```

장점:
- 용어 사전이 완전히 동기화됨
- 한 프로젝트에서 등록한 단어가 다른 프로젝트에서 즉시 사용 가능

### 7-2. 프로젝트별 분기

도메인이 전혀 다른 프로젝트는 branch로 분리:

```
glossary-repo/main        ← 공통 기반 (일반 프로그래밍 용어)
glossary-repo/trading      ← 거래 시스템 전용 확장
glossary-repo/web-app      ← 웹 앱 전용 확장
```

---

## 8. 운영 체크리스트

### 신규 프로젝트 초기 설정

- [ ] `git submodule add` 완료
- [ ] `.scan_list` 프로젝트 구조에 맞게 수정
- [ ] `.scan_ignore` 외부 종속성 제외 설정
- [ ] `python glossary/generate_glossary.py generate` 인덱스 생성
- [ ] `AGENTS.md`에 G-0, G-1 규칙 추가
- [ ] `.agents/workflows/new-identifier-procedure.md` 배치
- [ ] (선택) CI 스크립트 추가

### 일상 운영

- [ ] 신규 개발 시 `check-id` 실행
- [ ] 주기적 `scan_items.py` 실행으로 미등록 식별자 점검
- [ ] 서브모듈 버전 동기화: `git submodule update --remote`
- [ ] 사전 변경 후 `generate` 재실행

---

*문서 끝.*
