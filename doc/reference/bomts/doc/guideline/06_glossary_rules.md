# 06. 용어 관리 및 단어 사전 규칙 (Glossary v0.4)

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)
> 구조(root): `glossary/dictionary/words.json` + `glossary/dictionary/compounds.json`
> 정책(banned, pending): `glossary/dictionary/banned.json`, `glossary/dictionary/pending_words.json`
> 사람이 읽는 버전: `glossary/GLOSSARY.md`
> 생성물(term): `glossary/dictionary/terms.json` (자동 생성물, 참조 및 수동 편집 금지)

---

## ★ 절대 규칙 (Glossary v0.4 구조)

> 1. 식별자의 최소 단위(concept/root)는 **단어(word)**이다.
>    `glossary/dictionary/words.json`이 유일한 단어 기준이다.
> 2. 단어 조합이 고유한 도메인 의미를 가질 때만
>    **복합어(compound)**로 `glossary/dictionary/compounds.json`에 등록한다.
> 3. 사전에 없는 단어를 사용하려면 **사용자 제안/승인**이 필수다. 미등록 단어로 임의 개발 진행을 엄격히 금지한다 (**RULE G-1**).
> 4. 복수형, 약어 등 표현(variant)은 root 단어의 variant로 파생한다. 파생 규칙을 따르지 않고 plural(복수형) 자체가 root로 등록되는 것은 절대 불가하다. Variant가 직접 사용될 경우, normalize 가능 여부에 따라 WARN 또는 ERROR가 발생한다.
> 5. `glossary/dictionary/terms.json`은 생성물(projection)이다. 개발 도구(audit 등)는 terms.json을 직접 스캔하거나 Source of Truth로 참조해서는 안 되며, 반드시 index를 거쳐 root 기준으로 검사해야 한다.

---

## 1. 단어 vs 복합어 판단

### 새 식별자가 필요할 때

1. 식별자를 단어로 분해한다
   예: "entry_decision_logger" -> [entry, decision, logger]

2. 각 단어가 words.json에 있는가?
   - 모두 있음 -> 3단계로
   - 없는 단어 있음 -> 사용자 승인 받아 words.json에 등록

3. 이 조합이 복합어 등록 조건에 해당하는가?
   (a) 조합 의미 != 개별 단어 합 -> 등록
   (b) 도메인 공인 약어 필요 -> 등록
   (c) 금지 표현 구분 필요 -> 등록
   (d) 시스템 공식 객체명이더라도,
     - 단어 조합만으로 의미가 명확하면 등록하지 않는다.
     - 조합만으로 의미가 불명확하거나,
     - 혼동 가능성이 있을 때만 등록한다.
     ※ 주의: 공식 객체명이라는 이유만으로 복합어를 등록하지 않는다.
             불필요한 compound 등록은 glossary 팽창을 유발한다.
   (e) 외부 고유명사 -> 등록
   -> 해당 없음 -> 등록하지 않음. 조합 규칙으로 생성.

### 검증 도구 활용

```bash
# 식별자가 사전 기준에 맞는지 확인
python glossary/generate_glossary.py check-id <식별자>

# 미등록 단어 확인 + 등록 제안 생성
python glossary/generate_glossary.py suggest <식별자>
```

---

## 2. 식별자 포맷팅 규칙

(기존 §1과 동일 - 변경 없음)

| 사용 위치 | 포맷 | 조합 예시 |
|-----------|------|----------|
| 변수명 | snake_case | order_intent |
| 함수명 | snake_case | get_order_intent() |
| 클래스명 | PascalCase | OrderIntent |
| 모듈(파일)명 | snake_case | order_intent.py |
| DB 테이블명 | snake_case (단수형) | order_intent |
| DB 컬럼명 | snake_case | order_intent_id |
| 환경변수명 | UPPER_SNAKE_CASE | ORDER_INTENT |
| config 키 | snake_case | order_intent |

---

### 2-A. 허용 문자 및 구분자 규칙

모든 식별자는 다음 문자만 사용한다.

허용:
- a-z
- 0-9
- underscore (_)

금지:
- 하이픈 (-)
- 공백
- 기타 특수문자

규칙:
- snake_case: 소문자 + underscore만 사용
- PascalCase: 영문 대소문자만 사용 (구분자 없음)
- UPPER_SNAKE_CASE: 대문자 + underscore만 사용

예시:
- order_intent ✔
- OrderIntent ✔
- ORDER_INTENT ✔

금지 예시:
- order-intent ✖
- order intent ✖
- orderIntent (변수/함수 기준) ✖

---

## 3. 단어 순서 규칙 (신규)

| 순서 | 패턴 | 예시 |
|------|------|------|
| 수식어 -> 피수식어 | prefix/adj + noun | kr_stock, daily_report |
| 동사 -> 목적어 | verb + noun | get_position, close_trade |
| 주체 -> 역할 | noun + role | risk_manager, signal_engine |
| 범위(대) -> 범위(소) | scope + detail | market_session, account_snapshot |

---

## 4. 주요 단어 빠른 참조

(기존 §2 "주요 용어" -> words.json 기반으로 자동 갱신되는 구조로 전환)

> 아래는 예시이다. 전체 목록은 glossary/GLOSSARY.md를 참조한다.

### 마켓 접두사 (words.json, domain=market, pos=prefix)

| 단어 | 한글 | 약어 | 금지 표현 |
|------|------|------|----------|
| kr | 한국 | KR | korea, kor |
| us | 미국 | US | — |
| fx | 외환 | FX | — |
| crypto | 암호화폐 | CRYPTO | coin, virtual |

### 핵심 복합어 (compounds.json)

| 복합어 | 구성 | 한글 | camelCase | 약어 | 등록 사유 |
|--------|------|------|-----------|------|----------|
| stop_loss | stop+loss | 손절 | stopLoss | SL | 도메인 공인 약어 |
| take_profit | take+profit | 익절 | takeProfit | TP | 도메인 공인 약어 |
| kill_switch | kill+switch | 킬스위치 | killSwitch | KS | 프로젝트 고유 메커니즘 |
| order_intent | order+intent | 주문의도 | orderIntent | OI | 시스템 공식 모델명 |
| fx_futures | fx+futures | 외환선물 | fxFutures | FX_FUT | 혼동 방지 (vs MT5) |
| kr_stock | kr+stock | 한국주식 | krStock | KR_STOCK | 혼동 방지 (vs KIS) |

---

## 5. 금지 표현 (banned.json 참조)

(기존 §3 -> banned.json으로 데이터 이동. 이 섹션은 요약만.)

> 전체 목록: glossary/dictionary/banned.json

| 금지 표현 | 올바른 표현 | 이유 |
|-----------|------------|------|
| MT5, MT5_FUT (마켓 의미) | FX_FUT | MT5는 플랫폼, 마켓 아님 |
| KIS, KOSPI (마켓 의미) | KR_STOCK | KIS는 브로커명 |

---

## 6. 신규 단어 등록 절차

### 승인 레벨

| 작업 | 승인 | 이유 |
|------|------|------|
| 기존 단어 조합 -> 새 식별자 | 불필요 | 규칙 기반 조합 |
| words.json에 새 단어 추가 | **사용자 승인** | 사전 원자 단위 증가 |
| compounds.json에 복합어 추가 | **사용자 승인** | 공식 개념 등록 |
| 기존 단어/복합어 수정·삭제 | **사용자 승인** | 기존 코드 영향 |

### AI 에이전트 워크플로우

1. 새 식별자 필요 시 `check-id` 실행
2. 미등록 단어 발견 -> 사용자에게 승인 요청
3. 승인 후 words.json에 추가
4. 복합어 등록 조건 해당 시 -> 사용자에게 승인 요청
5. `python glossary/generate_glossary.py generate` 실행
6. `doc/change_log.md`에 기록

## 6-A. 신규 용어 미등록 시 강제 규칙

신규 식별자에 필요한 단어가 words.json에 없으면:

반드시 수행:
1. 단어 누락을 사용자에게 보고
2. words.json 등록 제안 생성
3. 승인 후에만 식별자 생성

금지:
- 유사 단어로 임의 대체
- 약어를 임의 생성
- 동일 개념에 서로 다른 용어 혼용

---

## 7. 약어 중복 관리

(기존 §4와 동일 원칙, words.json + compounds.json 양쪽 검증)

> validate 명령이 자동 검출한다:
> python glossary/generate_glossary.py validate

---

## 8. 단수형/복수형 사용 규칙

> 상세 근거: AGENTS.md Rule 8-A

### 8-1. words.json 등록 원칙

- words.json에는 **단수형**만 등록한다.
- 복수형은 `plural` 필드로 파생한다 (정규형이면 null, 불규칙이면 명시).
- 복수형을 별도 단어로 등록하는 것을 **금지**한다.
- 복수형이 없는 불가산 명사는 `plural: "-"`로 표시한다.

### 8-2. 복수형이 사용되는 곳 (코드 — 의미 기반)

| 패턴 | 예시 | 설명 |
|------|------|------|
| 컬렉션 변수 | `orders: list[Order]` | 복수형 사용 |
| 목록 반환 함수 | `list_orders()` | 복수형 사용 |
| 의미 suffix | `order_queue`, `execution_log` | 도메인 의미 추가 시에만 |
| 환경변수 (복수 값) | `EXCLUDE_DIRS` | 상황에 따라 판단 |

- suffix는 복수형의 대체 수단이 아니다
- suffix는 자료구조 타입 표현 목적으로 사용하지 않는다

### 8-3. 단수 강제 위치 (STRICT)

| 위치 | 근거 |
|------|------|
| 폴더명 | Rule 8-A §1 |
| DB 테이블명 | Rule 8-A §2 |

### 8-4. suffix 규칙

1. suffix는 기본적으로 사용하지 않는다
2. 복수형으로 충분하면 suffix 사용하지 않는다
3. suffix는 "역할/상태/의미"를 추가할 때만 사용한다
4. `_list`, `_array`, `_dict`는 구현 타입이라 기본적으로 비권장
5. 단, 구조 자체가 의미이거나 인터페이스 명세일 때만 예외 허용

**suffix 분류:**

강하게 추천 (도메인 의미):
- 상태/시점: `_snapshot`, `_state`, `_status`, `_cache`
- 기록/이력: `_log`, `_history`, `_record`, `_trace`
- 흐름/처리: `_queue`, `_stream`, `_pipeline`
- 관계/매핑: `_map` (허용 범위)
- 관리/집합: `_registry`, `_store`, `_pool`

조건부 허용:
- `_set` — 중복 제거가 의미적으로 중요할 때만
- `_map` — key-value 관계가 중요할 때만

기본적으로 비권장 (타입 중심):
- `_list`, `_array`, `_dict`, `_tuple`

`_list`/`_array`/`_dict` 예외 허용 조건:
- API 인터페이스 명세에서 타입을 명확히 해야 할 때
- 동일 개념 내 구분 필요 (order_queue vs order_list)
- 자료구조 자체가 도메인 개념일 때

### 8-4-1. suffix 사용 제한

복수형(`orders`)으로 의미가 충분한 경우 suffix(`order_list`) 사용 금지.
suffix + 복수형 중복 금지: `orders_list` ← 완전 오류.
기존 코드의 suffix는 유지하되 신규 코드에서 같은 패턴 확장 금지.

---

## 9. [N] 패턴 (숫자 포함 식별자)

### 9-1. 개요

숫자가 포함된 반복 식별자를 개별 등록하지 않고,
`[N]` 패턴으로 compounds.json에 한 번만 등록한다.

### 9-2. 등록된 [N] 패턴

| 패턴 | 한글 | 사용 예 | 설명 |
|------|------|---------|------|
| [N]m | N분봉 | 1m, 5m, 10m, 60m | N분 단위 캔들 데이터 |
| top[N] | 상위 N개 | top3, top5, top100 | 상위 N개 항목 선택 |

### 9-3. 규칙

1. [N]은 임의의 자연수 (> 0)
2. [N] 패턴은 compound에서만 사용 (word에는 불가)
3. 등록 시 description에 [N]의 정의를 반드시 기술
4. 실제 코드에서는 구체적 숫자로 치환: `bars_1m`, `top5_value`
5. `check-id` 실행 시 숫자 부분을 [N]으로 치환하여 매칭

### 9-4. 신규 [N] 패턴이 필요할 때

사용자 승인 후 compounds.json에 등록한다.
description에 [N]의 범위/의미를 반드시 명시한다.
