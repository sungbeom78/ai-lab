> 작업 시작 전 반드시 읽는 순서:
> 1. GEMINI.md (전역 규칙)
> 2. 이 문서 (프로젝트 규칙)
> 3. SOURCE_OF_TRUTH.md (데이터 소유권 + 인터페이스 잠금)
> 4. .agents/workflows/ (수행 절차)

# AI Guideline — BOM_TS (Trading System)

> Last updated: 2026-04-09  |  Version: 2.5.0
> Project: BOM_TS (Bomiyang Trading System)

---

## ⚠️ 이 문서는 BOM_TS 프로젝트에 적용되는 절대 지침입니다.
> GEMINI.md(전역 규칙)와 함께 적용됩니다.
> 충돌 시 이 문서가 BOM_TS 프로젝트 범위 내에서 우선합니다.
> 작업 시작 전 관련 항목의 상세 문서를 먼저 읽고 착수하십시오.

---

## 프로젝트 명칭 체계

| 레이어 | 명칭 | 사용 위치 |
|--------|------|-----------|
| 개발 내부 | `ts` | 디렉토리명, 코드 import, 파일명 |
| 시스템 공식 | `BOM_TS` | README, 지침 문서, 로그, 커밋 |
| 공개 웹 브랜드 | `Bomiyang's Trade System` | 웹페이지 타이틀, 헤더, 소개 문구 |

> 상세 규칙: [08_naming.md](guidelines/08_naming.md)

---

## 네이밍 정책 참조

> 신규 식별자 생성 전 glossary 검증은 AGENTS.md와 06_glossary_rules.md를 따른다.
> 네이밍 규칙은 AGENTS.md의 "NAMING CONSISTENCY RULE"을 따른다.
> 폴더 및 테이블 네이밍은 단수형이 강제되며, 세부 규칙은 AGENTS.md를 반드시 확인한다.

---

## 핵심 원칙 — AI 역할 제한

**AI = Analyst. 실시간 매매 개입 절대 금지.**

| AI가 할 수 있는 것 | AI가 할 수 없는 것 |
|--------------------|--------------------|
| 로그 분석 | 실시간 매매 판단 |
| 전략 성능 분석 | 주문 직접 실행 |
| 파라미터 추천 | 포지션 관리 |
| 백테스트 분석 | 리스크 한도 조정 |

---

## 지침 목록

| 파일 | 내용 | 참조 시점 |
|------|------|-----------|
| [01_execution.md](guidelines/01_execution.md) | 실행 진입점 규칙 (`run.py`, `run_test.py`) | 실행 관련 코드 작성 시 |
| [02_config.md](guidelines/02_config.md) | 설정 파일 역할 분리 (`.env` / `settings.yaml` / `trade.yaml`) | 설정값 추가·변경 시 |
| [03_git.md](guidelines/03_git.md) | Git 포함/제외 목록, 커밋 규칙 | 파일 추가·커밋 시 |
| [04_coding_standards.md](guidelines/04_coding_standards.md) | BOM_TS 코딩 표준 (예외 처리, 로깅) | 코드 작성 시 |
| [04_telegram_bot.md](guidelines/04_telegram_bot.md) | 텔레그램 봇 연동 규칙 | 알림 관련 작업 시 |
| [05_collectors.md](guidelines/05_collectors.md) | 수집기 추가 체크리스트 | 수집기 신규 추가 시 |
| [06_glossary_rules.md](guidelines/06_glossary_rules.md) | 단어 사전 규칙 (words.json 기반 식별자 생성) | 식별자 작성·변경 시 |
| [07_public_web.md](guidelines/07_public_web.md) | 공개 웹 개발·보안·업데이트 규칙 | 공개 웹 작업 시 |
| [08_naming.md](guidelines/08_naming.md) | 프로젝트 명칭 레이어 체계 | 명칭 표기 시 항상 |
| [09_data_flow.md](guidelines/09_data_flow.md) | 데이터 흐름 규칙 (레이어 경계, 소유권, 불변 조건) | **모든 코드 변경 시** |
| [10_qa.md](guidelines/10_qa.md) | QA 실행/운영 지침 (레벨, 텔레그램, 대응 규칙) | **개발 완료 시, 커밋 전, 운영 진입 시** |
| [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md) | SoT 선언표 + 인터페이스 잠금 | **모델/설정/저장소 변경 시** |

> Python 문법 오류 방지(f-string, `^` 줄바꿈), PEP8, 타입 힌트, 결정론 원칙은
> **GEMINI.md RULE 7 / RULE 8** 에서 관리합니다.

## 용어 관리 (Glossary v0.4 기준)

- 단어 사전 (`root`): `glossary/dictionary/words.json` (개념, 단수형, 원자 단위)
- 복합어 사전 (`root`): `glossary/dictionary/compounds.json` (도메인 공인 / 조건부 등록)
- 금지 표현 (`banned`): `glossary/dictionary/banned.json`
- 제안 보류 (`pending`): `glossary/dictionary/pending_words.json`
- 생성물 (`term`): `glossary/dictionary/terms.json` (자동 생성물, 절대 Source of Truth가 아님)
- 표현 (`variant`): 복수형(plural), 약어(abbreviation) 등은 root 단어의 variant로 파생한다. Variant가 root 대신 선언 사용될 경우 QA 단계에서 WARN/ERROR 처리된다.
- **필수 절차**: 신규 식별자 생성 전 반드시 `python glossary/generate_glossary.py check-id <identifier>` 를 실행하여 미등록 단어 발생 여부를 확인해야 한다. 미등록 단어 발생 시 즉시 식별자 생성을 중단하고 제안 요청(RULE G-1)을 통해 사용자 승인 또는 보류 판정을 받아야 한다.

---

## AI 수정 금지 구역 (Frozen Zones)

> 아래 항목은 **사용자 승인 없이 수정 불가**.
> 위반 시 즉시 작업 중단 후 사용자에게 보고.

| 파일/패턴 | 이유 |
|---------|------|
| `src/common/models.py` 공개 필드 | 전체 시스템 호환성 |
| `config/settings.yaml` 기존 키 이름 | 런타임 호환성 |
| `script/db/schema*.sql` 기존 컬럼 | DB 데이터 정합성 |
| `src/adapter/*/base.py` 공개 인터페이스 | 브로커 연동 안정성 |
| `src/storage/redis_client.py` 키 패턴 | 다중 소비자 호환 |

> 상세: [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md) § 6. 인터페이스 잠금

---

## 변경 전 체크리스트

코드를 변경하기 전에 아래 항목을 **반드시** 확인합니다.

```
□ 이 변경이 생성/수정하는 데이터의 소유 모듈은 어디인가? (SOURCE_OF_TRUTH.md)
□ 모듈 금지행위를 위반하지 않는가? (module_index.md > Forbidden)
□ 레이어 규칙을 위반하지 않는가? (09_data_flow.md)
□ 새 식별자의 구성 단어가 모두 words.json에 등록되어 있는가? (06_glossary_rules.md)
□ 폴더명/테이블명이 단수형인가? (Rule 8-A §1, §2)
□ 숫자 포함 식별자는 [N] 패턴에 매칭되는가?
□ 수정 금지 구역에 해당하는가? (위 표 확인 — 해당 시 STOP)
□ 해당 불변 규칙(INV-xxx)이 여전히 유효한가?
□ 관련 통합 테스트가 이 변경을 커버하는가?
□ 작업 완료 후 qa_quick을 실행했는가? (10_qa.md)
□ 커밋 전 qa_standard가 PASS인가? (10_qa.md)
```

---

## ⛔ 필수 동반 작업 — 절대 누락 금지

> **아래 규칙은 예외 없이 반드시 수행한다. 누락 시 작업 미완료로 간주한다.**

### RULE A: 설정 파일 수정 시 필수 동반 작업

`.env`, `config/settings.yaml`, `config/trade/*.trade.yaml` 수정 시 **반드시 아래 3가지를 동반**한다:

| 순서 | 동반 작업 | 상세 |
|------|-----------|------|
| 1 | **백업 생성** | `tmp/backup/config/{YYYYMMDD_HHmmss}/` 에 수정 전 파일 복사 |
| 2 | **example 파일 동기화** | `.env` → `.env.example` 구조 동기화 (값은 비워둠) |
|   |                        | `settings.yaml` → `settings.example.yaml` 구조 동기화 |
| 3 | **change_log 기록** | `doc/change_log.md` 에 변경 사항 기록 |

> `.example` 파일에는 **실제 값(비밀번호, 키 등)을 절대 넣지 않는다.**
> 상세 수행 절차: `.agents/workflows/edit-file-procedure.md`

---

### RULE B: 소스 코드 수정 시 qa_quick 필수 실행

소스 코드(`src/` 하위)를 수정한 경우 **반드시** 작업 마무리 시점에 아래를 실행한다:

```bash
python run_test.py qa_quick
```

- PASS가 아니면 원인을 해결한 뒤 재실행한다.
- qa_quick 실행 없이 작업 완료 보고를 하지 않는다.
- 소스/스키마 변경 시, 변경 파일 대상 identifier audit를 `qa_quick`에서 반드시 수행한다.

---

### RULE C: SSOC — Single Source of Computation (단일 연산 원칙)

> **"데이터가 틀어지는 건 느린 것보다 나쁘다."**

#### 절대 금지
동일 의미의 데이터를 2곳 이상에 저장하는 행위를 금지한다.
(예: raw 데이터 + 카운터 변수, 리스트 + 합산 변수)

#### 원칙
- 보유 종목수, 거래 횟수, 승률, 카운트 등 **파생 가능한 값은 별도 변수에 저장하지 않는다.**
- 필요한 시점에 **원본 컬렉션(list, deque, dict)에서 직접 연산**한다.
- 제한 조건 확인 시 `any()` / short-circuit으로 "N개 이상 존재 여부"만 확인한다.

| 판정 | 패턴 |
|------|------|
| ❌ 금지 | `self._entry_count += 1` (상태 카운터 변수) |
| ❌ 금지 | `self._daily_total_buys` (전체 합산 전용 변수) |
| ✅ 허용 | `open_count = len(...)` (함수 내 로컬, 스코프 밖 저장 금지) |
| ✅ 허용 | `sum(1 for t in trades if t.symbol == sym)` (조회 시 연산) |
| ✅ 허용 | `any(t.market == M for t in active_list)` (존재 여부만 확인) |

#### 예외 (카운터 허용 조건)
1. 원본 데이터가 존재하지 않는 경우 (이벤트 스트림만 있고 저장 안 하는 경우)
2. 위 예외에 해당하더라도, **반드시 코드 주석으로 사유를 명시**해야 한다

---

### RULE D: 마켓 분리 규칙

#### 원칙
- KR, US, FX, CRYPTO 등 마켓별 상태는 **개별 변수로 분리하지 않는다.**
- 반드시 `dict[market]` 형태로 관리한다.
- 전체 합산은 조회 시 `sum(dict.values())` 등으로 계산한다.

| 판정 | 패턴 |
|------|------|
| ❌ 금지 | `kr_active_count`, `us_active_count` (변수 분리) |
| ❌ 금지 | `_daily_total_buys` (전체 합산 전용 변수) |
| ✅ 허용 | `active_trades[market]` (dict로 마켓별 관리) |
| ✅ 허용 | `sum(len(v) for v in data.values())` (조회 시 합산) |

---

### RULE E: 마켓별 런타임 데이터 구조 및 사용 지침

#### Authoritative Runtime Dict 체계

런타임에서 기준이 되는 데이터 구조는 정확히 아래 4개다.
이 외 별도 summary/state dict 생성은 금지한다.

| Dict | 소유 모듈 | 역할 |
|------|----------|------|
| `today_trading_by_market[market]` | `execution/orchestrator` | 당일 거래 이벤트 (포지션, 주문, 체결) |
| `account_by_market[market]` | `execution/orchestrator` | 계좌 상태 (잔고, 증거금) |
| `symbol_index_by_market[market]` | `selector` + `orchestrator` | 종목 메타 정보 |
| `pipeline_by_market[market]` | `selector` + `signals` | 스캔/필터/스코어 파이프라인 상태 |

#### 데이터 접근 규칙
- 데이터 접근은 직접 dict 탐색하지 않고 **전용 함수로 수행**한다.
- 구조 변경 시 영향 범위를 최소화하기 위함이다.
- `report/` 레이어는 `execution/` 상태만 읽기 전용으로 접근한다. (09_data_flow.md 참조)

---

### RULE F: 파일 인코딩 표준 — 절대 준수

> **모든 파일 생성/수정 시 예외 없이 적용한다.**
> 상세 수행 절차: `.agents/workflows/edit-file-procedure.md § 0. 인코딩 표준`

#### 표준

| 항목 | 표준값 |
|------|--------|
| 인코딩 | **UTF-8, No BOM** |
| 줄바꿈 | **LF** (`\n` 만 허용, CRLF 금지) |
| 최종 줄 | 빈 줄 1개로 종료 |

#### 위반 시 결과
- QA `encoding_bom::*` → **CRITICAL** 실패
- QA `encoding_eol::*` → **CRITICAL** 실패
- 한글 포함 파일이 cp949로 저장되면 `\xc2\x80` 오류 바이트가 삽입되어 한글 손상

#### 준수 규칙 (우선순위 순)

1. `write_to_file` / `replace_file_content` 도구 → UTF-8 LF 자동 보장
2. Python으로 파일을 직접 쓸 때: `open(path, 'wb').write(content.encode('utf-8'))`
3. **절대 금지**: PowerShell `Set-Content`, `Add-Content`, `Out-File` 기본값 (cp949/UTF-16 삽입), `open(path, 'w', encoding='utf-8-sig')` (BOM 삽입)

#### 검증 명령 (파일 수정 완료 시 필수)

```bash
python tool/check_encoding.py
```

`All encoding checks passed` 가 아니면 **작업 완료로 보고하지 않는다**.
