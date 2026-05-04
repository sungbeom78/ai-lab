# 08. 프로젝트 명칭 체계

> 문서 위치: `doc/guideline/08_naming.md`
> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)

---

## ★ 절대 규칙

> 명칭은 사용 레이어에 따라 구분한다.
> 레이어 간 혼용 금지. 웹 공개 텍스트에 `ts`를 그대로 노출하지 않는다.
>
> 1. plural root 금지: 복수형은 항상 `variant`로 취급하며 단수형 root에서 파생한다.
> 2. variant는 root로 normalize 될 수 있어야 한다. Variant가 코드 상에 변수 이름으로 사용될 시 WARN 및 ERROR 처리를 받을 수 있다.
> 3. abbreviation(약어)은 glossary에 명시된 정의에 따라서만 허용된다. 임의의 약어 생성은 절대 금지한다.

---

## 1. 명칭 레이어 체계

| 레이어 | 명칭 | 사용 위치 |
|--------|------|-----------|
| 개발 내부 | `ts` | 디렉토리명, 코드 import, 파일명, 내부 스크립트 |
| 시스템 공식 | `BOM_TS` | README, 지침 문서, 환경변수 prefix, 로그 메시지, 커밋 메시지 |
| 공개 웹 브랜드 | `Bomiyang's Trade System` | 대시보드 헤더, 웹 타이틀, 소개 문구, /docs 페이지 상단 |

### 사용 예시

```
# ✅ 올바른 사용

# 개발 내부 (코드)
from ts.src.trading_signal import KrSignalEngine
PROJECT_ROOT = Path("~/ts")

# 시스템 공식 (문서·로그)
# Project: BOM_TS
logger.info("BOM_TS started")
# README 상단: BOM_TS v2.0

# 공개 웹 브랜드 (HTML·템플릿)
<title>Bomiyang's Trade System</title>
<h1>Bomiyang's Trade System</h1>

# ❌ 금지
<h1>ts Trading System</h1>       # 개발 내부 명칭을 웹에 노출
<h1>antigravity</h1>             # 구 명칭 사용
logger.info("antigravity started") # 구 명칭 사용
```

---

## 2. 구 명칭 → 신 명칭 매핑

| 구 명칭 | 신 명칭 | 적용 레이어 | 비고 |
|---------|---------|------------|------|
| `antigravity` (시스템명) | `BOM_TS` | 시스템 공식 | 문서·로그·README |
| `antigravity` (웹 표기) | `Bomiyang's Trade System` | 공개 웹 브랜드 | 웹페이지 노출 텍스트 |
| `antigravity Trading Platform` | `Bomiyang's Trade System` | 공개 웹 브랜드 | 웹페이지 푸터·타이틀 |
| `ts1` (구 디렉토리) | `ts` | 개발 내부 | 이미 리팩토링 완료 기준 |
| `Project: antigravity/ts` | `Project: BOM_TS` | 시스템 공식 | README 상단 표기 |

> `antigravity`는 외부 도구/라이브러리 이름으로 계속 존재할 수 있으나,
> **이 시스템의 명칭으로는 사용하지 않는다.**

---

## 3. 변경이 필요한 파일 목록

### 3-1. 문서 (doc/)

| 파일 | 변경 내용 |
|------|-----------|
| `README_AI_GUIDELINE.md` | 상단 `Project: antigravity/ts` → `Project: BOM_TS` |
| `guidelines/01_execution.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/02_config.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/03_git.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/04_coding_standards.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/05_collectors.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/06_glossary_rules.md` | 본문 `antigravity` → `BOM_TS` |
| `guidelines/07_public_web.md` | `antigravity` → `BOM_TS` / `Bomiyang's Trade System` (위치별 구분) |
| `module_index.md` | 프로젝트명 언급 부분 |
| `change_log.md` | 명칭 변경 항목 추가 (아래 양식 참고) |

### 3-2. 공개 웹 HTML/템플릿

| 위치 | 변경 전 | 변경 후 |
|------|---------|---------|
| `<title>` 태그 | `antigravity` | `Bomiyang's Trade System` |
| 대시보드 헤더 `<h1>` | `⚡ antigravity` | `Bomiyang's Trade System` |
| `/docs/*` 페이지 상단 | `antigravity` | `Bomiyang's Trade System` |
| 푸터 표기 | `antigravity Trading Platform` | `Bomiyang's Trade System` |
| 프로젝트 소개 문구 | `antigravity는 개인 자동매매...` | `Bomiyang's Trade System은 개인 자동매매...` |

### 3-3. 소스 코드 (문자열·주석만)

> 클래스명·함수명·변수명 등 로직에 영향을 주는 식별자는 변경하지 않는다.
> 아래는 **로그 메시지, 주석, 시작 배너 문자열**에만 해당한다.

| 위치 | 변경 내용 |
|------|-----------|
| `app.py` 시작 배너 | `antigravity started` → `BOM_TS started` |
| 로그 메시지 내 시스템명 | `antigravity` → `BOM_TS` |
| 코드 주석 내 프로젝트명 | `antigravity` → `BOM_TS` |

### 3-4. 변경하지 않는 것

```
✅ 유지
- 디렉토리명: ts/ (개발 내부 명칭, 현행 유지)
- 클래스명: KrSignalEngine, FxSymbolRanker, KisAdapter 등
- 환경변수 기존 키: KIS_AK, PG_DSN, REDIS_URL 등
- 브로커 관련 식별자: MT5, KIS, kis_adapter 등
- references/ 하위 외부 API 스펙
- Git 커밋 히스토리 (rewrite 금지)
```

---

## 4. change_log.md 추가 양식

아래 내용을 `doc/change_log.md` 최상단에 추가한다.

```markdown
## [2026-03-20] 프로젝트 명칭 체계 정립

### 변경 사항
- 명칭 레이어 3단계 구조 도입
  - 개발 내부: `ts` (현행 유지)
  - 시스템 공식: `BOM_TS` (BOMiyang's Trade System)
  - 공개 웹 브랜드: `Bomiyang's Trade System`
- 구 명칭 `antigravity` (시스템명 용도) 사용 중단

### 변경 이유
- `antigravity`는 외부 도구명과 혼동 가능
- 개인 브랜드(봄이양)를 반영한 명칭으로 정체성 명확화
- 레이어별 명칭 분리로 내부 코드 변경 없이 공개 브랜드 관리 가능

### 영향 범위
- doc/ 전체 문서 (코드 로직 변경 없음)
- 공개 웹 페이지 텍스트
- 로그 메시지·주석
```

---

## 5. AI 작업 명령 (Gemini / Claude 전달용)

새 작업 세션 시작 시 아래 내용을 프롬프트 앞에 붙여서 전달한다.

---

```
[BOM_TS 명칭 체계 적용 지시]

이 프로젝트는 명칭 레이어가 3단계로 구분됩니다.
모든 작업에서 아래 규칙을 반드시 준수하십시오.

■ 명칭 레이어 규칙

1. 개발 내부 명칭: ts
   - 디렉토리명, import 경로, 파일명, 내부 스크립트에만 사용
   - 예: from ts.src.trading_signal import ..., PROJECT_ROOT/ts/

2. 시스템 공식 명칭: BOM_TS
   - README, 지침 문서, 로그 메시지, 커밋 메시지에 사용
   - 예: "BOM_TS started", "Project: BOM_TS"

3. 공개 웹 브랜드명: Bomiyang's Trade System
   - 웹페이지 타이틀, 헤더, 소개 문구에만 사용
   - 예: <title>Bomiyang's Trade System</title>

■ 금지 사항

- 웹 공개 텍스트에 'ts' 직접 노출 금지
- 'antigravity'를 이 시스템의 명칭으로 사용 금지
- 세 레이어 명칭 혼용 금지
  (예: 웹에 'BOM_TS' 노출, 코드 주석에 'Bomiyang's Trade System' 사용 금지)

■ 현재 작업에서 생성하는 모든 산출물에 위 규칙을 적용할 것
```

---

## 6. 명칭 체계 요약 (빠른 참조)

```
┌─────────────────────────────────────────────────────┐
│                   명칭 레이어 구조                    │
├──────────────┬──────────────────────┬────────────────┤
│  레이어      │  명칭                │  사용 위치     │
├──────────────┼──────────────────────┼────────────────┤
│  개발 내부   │  ts                  │  코드, 경로    │
│  시스템 공식 │  BOM_TS              │  문서, 로그    │
│  공개 브랜드 │  Bomiyang's Trade    │  웹페이지      │
│              │  System              │                │
└──────────────┴──────────────────────┴────────────────┘
```
