> **PROJECT_CHARTER.md v2.0 takes precedence over this file.**
> Conflict order: PROJECT_CHARTER > .gemini/user_rules.md > .agents/workflows/ > GEMINI > AGENTS > guideline > judgment
> v2 (2026-04-30): Several rules in this file are now enforced through
> token-gated workflows and pre-commit hooks.
> Before code work:
>   python script/operation/charter/prior_art_check.py "<keyword>"
> Before commit:
>   python script/operation/charter/run_qa_quick_token.py
> Commits are blocked by `charter-prior-art-token` and
> `charter-qa-quick-token` when either token is missing or expired.

> 적용 도구: OMX (oh my codex) / Codex CLI
> 전역 규칙(GEMINI.md)과 함께 적용됩니다.

---

<!-- AUTONOMY DIRECTIVE — DO NOT REMOVE -->
YOU ARE AN AUTONOMOUS CODING AGENT.
YOU MUST COMPLETE TASKS WITHOUT UNNECESSARY INTERRUPTION.
ALL CORE RULES ARE MANDATORY AND NON-NEGOTIABLE.
<!-- END AUTONOMY DIRECTIVE -->

---

## 0. SYSTEM PRIORITY

System integrity is ALWAYS more important than speed.

| Priority | Violation Type | Consequence |
|----------|---------------|-------------|
| CRITICAL | Breaking architecture / data flow | SYSTEM FAILURE — STOP |
| CRITICAL | Modifying a Frozen Zone without approval | SYSTEM FAILURE — STOP |
| ERROR    | Violating rules | SYSTEM ERROR — FIX BEFORE PROCEEDING |
| OK       | Slow execution | Acceptable |
| NEVER    | Incorrect execution | NOT acceptable |

---

## 0-A. PRIME DIRECTIVES

### P1. 안전이 속도를 이긴다 (Safety Over Speed)
**"돌아가는 코드"보다 "실패할 때 스스로 멈추는 코드"가 우선이다.**
자동매매는 버그 = 실제 금전 손실이다. 기능 추가보다 방어 체계가 항상 우선한다.

### P2. 명시적인 것이 암묵적인 것보다 낫다 (Explicit Over Implicit)
타입, 의존성, 부작용, 기본값 — 모두 명시적으로 드러내야 한다. **"알아서 처리됨"은 금지어다.**

### P3. 모든 변경은 가역적이어야 한다 (Everything Reversible)
Feature Flag, Git 태그, DB 백업 없이는 실거래 영향 코드를 배포하지 않는다.

### P4. 경계를 신뢰하지 않는다 (Trust No Boundary)
외부 API, 설정 파일, DB, 다른 모듈 — 모든 경계에서 **데이터 타입과 유효성을 검증**한다.

### P5. 회고 없는 수정은 없다 (No Fix Without Learning)
모든 버그 수정에는 **회귀 테스트**와 **원인 분석 기록**이 따라야 한다.


---

## 1. DOCUMENTATION FIRST (MANDATORY)

The `doc/` directory is the SINGLE SOURCE OF TRUTH.

Before ANY code modification, read in this order:

1. `doc/README_AI_GUIDELINE.md`
2. `doc/SOURCE_OF_TRUTH.md`
3. `doc/module_index.md` (affected area)
4. Relevant `doc/guideline/` files

Identify:
- Affected modules and their owners
- Data flow constraints
- Frozen Zones (modification requires approval)

STRICT RULES:
- NEVER modify code without understanding documentation.
- NEVER assume behavior when documentation exists.
- If documentation is missing → PROCEED with minimal inference, CREATE docs AFTER, REPORT what was inferred.

---

## 1-A. PRIOR ART CHECK (MANDATORY, ENFORCED v2)

Every code-affecting task starts with one command:

    python script/operation/charter/prior_art_check.py "<keyword>"

This single command performs:
- cache/task/registry.md: in_progress task search
- doc/change_log.md: last 7 days, keyword grep
- doc/change_log_archive/: last 30 days
- doc/SOURCE_OF_TRUTH.md: relevant Frozen Zone awareness
- doc/module_index.md: module location
- doc/README_AI_GUIDELINE.md: existence check

Output: findings + session token at cache/task/.prior_art_<timestamp>.lock

The session token has 60-minute lifetime. The pre-commit hook
`charter-prior-art-token` checks for a fresh token before allowing commit.
No token = no commit.

This means:
- "긴급 핫픽스라서 절차 생략"은 불가능. 30초 안 걸린다.
- "registry 깜빡했다"는 발생 자체가 차단된다.
- "동일 영역 최근 수정 못 봤다"도 차단된다.

If prior_art_check reports an active in_progress task on the same area,
read its handoff.md before proceeding. If it reports a Frozen Zone overlap
warning, stop and request user approval.

---

## 2. MINIMUM SCOPE (MANDATORY)

After documentation review:
- Inspect ONLY required files.
- Do NOT scan the entire codebase unnecessarily.
- If context is insufficient → expand scope progressively, one file at a time.

---

## 3. DUPLICATE PREVENTION (MANDATORY)

Before creating ANY new variable, function, class, or module:

1. Search existing codebase for same or similar name.
2. Search existing codebase for same or similar responsibility.
3. **Search glossary (`words.json`, `compounds.json`) for same or similar meaning.**
   → 같은 의미의 기존 등록 단어가 있으면 반드시 그 단어를 사용한다. (Rule G-0 참조)
4. If found → REUSE or EXTEND. Do NOT create a duplicate.
5. If creating new → state explicitly:
   - Why existing code cannot be reused
   - Why existing glossary terms cannot be used
   - Where the new code is placed
   - What naming convention was followed

FORBIDDEN:
- Creating a second function that does what an existing one does
- Creating a new class with overlapping responsibility
- Using similar-but-different names for the same concept
  (e.g. `get_position` / `fetch_position` / `load_position` for the same thing)
- Using a synonym when an equivalent term is already registered in the glossary
  (e.g. `transmit` when `send` is registered, `abort` when `cancel` is registered)

---

## 4. WORKFLOW COMPLIANCE (ABSOLUTE)

Project workflows in `.agents/workflows/` are MANDATORY.
OMX skills in `~/.agents/skills/` are SUPPLEMENTARY.
Project workflows take precedence over OMX skills.

Applicable workflows:
- `change-code-procedure.md`
- `edit-file-procedure.md`
- `safe-command-policy.md`
- `new-identifier-procedure.md`
- `task-management-procedure.md`

RULES:
- Workflow overrides personal judgment.
- Workflow steps MUST NOT be skipped.
- If conflict occurs → follow RULE priority and REPORT.

---

## 5. DOCUMENTATION UPDATE (MANDATORY)

After ANY non-trivial change, update:
- `doc/module_index.md` — when modules/classes/responsibilities change
- `doc/change_log.md` — after every meaningful code change

Each update MUST include: purpose, affected files, data flow impact.
NEVER skip.

---

## 6. SAFETY RULES (STRICT)

STRICTLY FORBIDDEN:
- Hardcoded credentials, paths, API keys, or secrets in code
- Mixing live/paper trading logic in the same execution path
- Modifying Frozen Zones without explicit user approval

ALL values MUST come from:
- `.env` (sensitive / environment-specific)
- `config/settings.yaml` (tunable parameters)
- `config/trade/*.trade.yaml` (market-specific strategy config)

---

## 6-A. ENVIRONMENT CONFIRMATION GATE (MANDATORY)

Before ANY code path that touches order execution:

MUST confirm:
1. `TRADING_ENV` = `"paper"` or `"live"`
2. Broker connection target matches `TRADING_ENV`
3. If `TRADING_ENV` is missing or ambiguous → HALT. Do NOT proceed.

CORRECT gate pattern:
```python
env = os.getenv("TRADING_ENV")
if env not in ("paper", "live"):
    raise EnvironmentError(f"TRADING_ENV invalid: {env!r}")
```

FORBIDDEN:
- Assuming environment from context
- Defaulting to `"live"` silently
- Skipping environment check in test scenarios

---

## 6-B. DATA BOUNDARY & TYPE SAFETY

#### 1.1 모든 함수/메서드는 타입 힌트를 가진다 [MUST]
```python
# ❌ 금지
def get_position(ticket):
    ...

# ✅ 필수
def get_position(ticket: int) -> Position | None:
    ...
```

#### 1.2 Pyright strict 모드를 핵심 모듈에서 통과시킨다 [MUST]
- `src/core/**`, `src/markets/**` — strict 모드
- 실패한 타입 검사는 **merge 차단 사유**이다.

#### 1.3 `Any` 사용 금지 원칙 [SHOULD]
- `Any`가 필요한 경우 반드시 주석으로 사유 기록
- 외부 라이브러리 응답은 Pydantic으로 검증 후 구체 타입으로 변환

```python
# ❌ 금지
def process(data: Any) -> Any:
    ...

# ✅ 허용 (사유 명시)
def _raw_mt5_response(self) -> Any:
    """MT5 SDK가 dict | tuple | None을 섞어 반환함. 즉시 Pydantic으로 검증됨."""
    return mt5.history_deals_get(...)
```

---

### DATA BOUNDARY — 🔴 최우선

#### 2.1 모든 외부 경계는 Pydantic 관문을 통과한다 [MUST]

외부 경계란:
- 외부 API 요청/응답 (MT5, KIS, Upbit, IBKR 등)
- 설정 파일 로드
- DB 읽기/쓰기
- 메시지 큐
- 파일 I/O

```python
# ❌ 금지 — 원시 dict로 내부 전달
def get_deal(ticket):
    raw = mt5.history_deals_get(ticket=ticket)
    return raw  # 🚨 타입이 뭔지 모름, 내부에 전파됨

# ✅ 필수 — 경계에서 검증
def get_deal(ticket: int) -> Deal:
    raw = mt5.history_deals_get(ticket=ticket)
    return Deal.model_validate(raw)  # 타입 보장, 오류 시 즉시 실패
```

#### 2.2 strict=True 및 frozen=True 권장 [SHOULD]

```python
class Deal(BaseModel):
    model_config = {
        "strict": True,    # 타입 자동 변환 금지 ("1234" → 1234 변환 안 됨)
        "frozen": True,    # 불변 객체
        "extra": "forbid", # 예상 못한 필드 금지
    }
```

#### 2.3 데이터 흐름의 첫 관문에서 실패한다 (Fail at Entry) [MUST]

```python
# ❌ 금지 — 깊숙이 들어가서 실패
def orchestrate(ticket):
    _deep_call_1(ticket)
    _deep_call_2(ticket)
    mt5.history_deals_get(ticket=ticket)  # 🚨 여기서 침묵 실패

# ✅ 필수 — 진입 즉시 검증
def orchestrate(ticket: int):
    validated = TicketModel(ticket=ticket).ticket  # 🛡 여기서 즉시 실패
    _deep_call_1(validated)
    ...
```


---

## 7. CHANGE DISCIPLINE

- Prefer incremental changes.
- NEVER silently overwrite existing logic.
- NEVER remove logic without justification.
- If replacing → mark previous logic as deprecated explicitly, log in change_log.md.

---

## 8. CONFLICT HANDLING

If a conflict between rules or requirements occurs:
1. Follow RULE priority (this file > GEMINI.md > OMX defaults).
2. Continue execution.
3. REPORT the conflict explicitly in output.

DO NOT stop silently or ignore rules.

---

## 8-A. NAMING CONSISTENCY RULE (ABSOLUTE)

This rule defines **non-negotiable naming constraints** for structural stability.

### 1. Folder Naming (MANDATORY)
* ALL directory names MUST use **singular form**.
* NO exceptions.
* Plural directory names are considered **system inconsistency** and MUST be refactored.

Examples:
* `logs` → `log`
* `scripts` → `script`
* `tests` → `test`
* `tools` → `tool`
* `guidelines` → `guideline`

---

### 2. Table Naming (MANDATORY)
* ALL database table names MUST use **singular form**.
* NO exceptions.
* This applies to:
  * SQL schema
  * ORM models
  * repository layer

---

### 3. Code Naming (CONTROLLED FLEXIBILITY)

For the following:
* variables
* functions
* classes
* environment variables
* JSON / API fields

Naming MUST follow **data semantics**, not forced singularity.

RULE:
* Single object → singular
* Collection (list, set, dict, array) → plural

Examples:
```python
order = Order()
orders = list[Order]
```

FORBIDDEN:
```python
order = []       # ❌ wrong
orders = Order() # ❌ wrong
```

---

### 4. Naming Stability Rule (CRITICAL)

Once a name is defined in code:
* DO NOT rename for style or consistency.
* DO NOT convert singular ↔ plural later.
* Renaming is allowed ONLY IF:
  * it fixes a functional bug
  * or breaks semantics

Reason:
* Renaming introduces regression risk and breaks traceability.

---

### 5. Scope of Enforcement

| Area      | Rule                   |
| --------- | ---------------------- |
| Folder    | STRICT (singular only) |
| Table     | STRICT (singular only) |
| Code      | SEMANTIC               |
| File name | FLEXIBLE               |

---

### 6. Violation Handling

If violation is detected:
* Folder/Table → MUST FIX immediately
* Code naming → DO NOT refactor unless critical

---

## 8-B. GLOSSARY VALIDATION GATE (ABSOLUTE)

Before creating or renaming ANY identifier, glossary validation is mandatory.

### 1. Glossary v0.4 Structure
- **root**: 개념 (concept) - `words.json`, `compounds.json`
- **variant**: 표현 (plural, abbreviation, etc.)
- **term**: projection (생성물 - `terms.json`은 절대 Source of Truth가 아님)
- **banned**: 정책 (policy - `banned.json`)
- **pending**: 제안 보류 목록 (`pending_words.json`)

### 2. Scope of Application
- folder, file, module, class, function, variable, database table, database column, config key, environment variable, JSON/API field

### 3. RULE G-0: 기존 등록 용어 우선 사용 (MANDATORY — BEFORE G-1)

**새 식별자를 만들기 전에, 동일하거나 유사한 의미의 단어가 이미 등록되어 있는지 반드시 확인한다.**

절차:
1. 사용하려는 단어의 **의미/역할**을 정의한다.
2. `words.json`, `compounds.json`, `variant_map.json`에서 **같은 의미의 기존 단어**를 검색한다.
3. 기존 단어가 있으면 → **반드시 그 단어를 사용한다.** 새 동의어를 등록하지 않는다.
4. 기존 단어가 없을 때만 → G-1 절차(신규 용어 제안)로 진행한다.

FORBIDDEN:
- `send`가 등록되어 있는데 `transmit`, `dispatch`, `deliver`를 새로 등록하는 행위
- `error`가 등록되어 있는데 `fault`, `failure`를 동의어로 추가하는 행위
- 동일 개념에 대해 모듈마다 다른 단어를 사용하는 행위
  (예: A 모듈은 `cancel`, B 모듈은 `abort`, C 모듈은 `revoke`)

판단 기준:
- **"이 단어 없이, 기존 등록 단어만으로 식별자를 구성할 수 있는가?"**
- YES → 기존 단어를 사용. 신규 등록하지 않는다.
- NO  → G-1 절차로 진행.

### 4. RULE G-1: 신규 용어 제안 규칙 (MANDATORY)

The agent MUST run glossary validation before creating a new identifier:
```bash
python glossary/generate_glossary.py check-id <identifier>
```

If the validation detects an unregistered word (`[ERROR] 미등록`):
👉 **개발 즉시 중단 (HALT DEVELOPMENT)**

1. **먼저 기존 등록 단어로 대체 가능한지 검토한다 (G-0 준수).**
2. 대체 불가능한 경우에만 아래 포맷으로 승인을 요청한다:
   ```text
   [신규 용어 제안]
   | word | type | 의미 | 기존 유사어 검토 결과 | 위치 |
   |------|------|------|---------------------|------|
   ```
3. Wait for user decision:
   - **승인(Approve)**: word is registered, proceed.
   - **보류(Pending)**: word is added to `pending_words.json`, development proceeds (will raise WARN in QA).
   - **거부(Reject)**: naming must be changed.

### 4. Plural & Variant Control
* words.json에 복수형을 독립 단어로 등록하지 않는다.
* 복수형은 plural 필드에서 파생한다.
* 폴더명/테이블명은 항상 단수 (Rule 8-A §1, §2).
* 코드는 의미 기반 — 컬렉션이면 복수 허용.
* suffix는 도메인 의미 추가 시에만 사용 (_queue, _log, _snapshot 등).
* suffix (_list, _array, _dict 등)는 자료구조 타입 표현 목적으로 사용하지 않는다.
* 기존 코드의 suffix는 유지하되, 신규 코드에서 확장 금지.
* 숫자 포함 식별자(1m, top5)는 [N] 패턴으로 처리. 개별 등록 금지.
* **Variant Usage Validation**: 복수형, 약어 등의 variant가 root 대신 직접 사용된 경우 자동 normalize가 가능하면 WARN, 의미 충돌 가능성이 있으면 ERROR 처리된다.
* 검증: `python glossary/generate_glossary.py validate`

---

## 9. VERIFICATION (MANDATORY)

Before reporting completion:
- Validate logic.
- Run tests if available.
- Ensure no regression.

TRADING-SPECIFIC:
- Verify order quantity / price calculation with sample data.
- Confirm stop-loss / risk limits are applied.
- Confirm no unintended position would be opened.

---

## 9-A. REGRESSION VERIFICATION (MANDATORY)

After ANY change, before reporting complete:

1. Identify what existing behavior this change could break.
2. Run the minimum test that covers that behavior.
3. Attach the result.

If no test exists for the affected behavior:
→ CREATE a minimal test first.
→ THEN make the change.
→ THEN verify.

* If a task adds or modifies identifiers, targeted glossary audit for the changed files is mandatory before completion.

"테스트가 없어서 확인 불가"는 완료 사유가 아니다.
테스트를 먼저 만드는 것이 작업의 일부다.

---

## 9-B. TEST & ARCHITECTURE RULES

#### 3.1 "테스트 없음 = 완료 안 됨" [MUST]
- 새 기능, 버그 수정, 리팩토링 — 모두 테스트 필수
- "테스트가 없어서 확인 불가"는 **완료 사유가 아니다**.

#### 3.2 비정상 시나리오 테스트 필수 [MUST]

```python
# 새 함수를 만들 때는 아래를 반드시 함께 작성:
# 1) 정상 케이스
# 2) 경계값 (0, 빈 값, 최대값)
# 3) 잘못된 타입 (문자열, None, 음수 등)
# 4) 외부 의존성 실패 (타임아웃, 잘못된 응답)
```

#### 3.3 버그 수정은 회귀 테스트를 동반한다 [MUST]
- 버그가 재현되는 테스트를 **먼저** 작성
- 해당 테스트가 실패하는 것을 확인한 후
- 코드를 수정하여 테스트를 통과시킨다
- 커밋 메시지에 `fixes: #이슈번호` 포함

#### 3.4 커버리지 기준 [MUST]
- `src/core/` — 90% 이상
- `src/markets/` — 80% 이상
- 기타 — 60% 이상
- 커버리지 하락 PR은 merge 차단

---

### § 4. 아키텍처 규칙

#### 4.1 단일 책임 원칙 (SRP) [MUST]
- **하나의 클래스/모듈은 하나의 변경 이유만 가진다**
- `orchestrator.py` 같은 God Class 금지
- 500 라인 초과 파일은 리팩토링 후보

#### 4.2 의존성 역전 [MUST]
- 구현체 직접 import 금지, 추상 인터페이스(ABC/Protocol) 의존
- 생성자 주입으로 의존성 전달

```python
# ❌ 금지
class Orchestrator:
    def __init__(self):
        self.mt5 = MT5Adapter()  # 하드코딩

# ✅ 필수
class Orchestrator:
    def __init__(self, broker: Broker):  # 추상 의존
        self.broker = broker
```

#### 4.3 상태 변경은 한 곳에서 [MUST]
- DB 쓰기는 Repository 계층에서만
- 전역 상태 변경은 `JournalWriter`를 경유
- 암묵적 side effect 금지 (getter가 write하는 등)

#### 4.4 순환 의존성 금지 [MUST]
- `core → markets` 방향만 허용
- `markets → core` 방향 import 금지 (인터페이스만 의존)


---

## 10. AUTONOMY POLICY

DO NOT ask for confirmation except:
- Destructive or irreversible operations
- Major architectural changes
- Any modification to:
  - Order execution logic
  - Position sizing logic
  - Risk management rules
  - API key / broker connection config
  - Frozen Zones (see README_AI_GUIDELINE.md)

Otherwise → PROCEED.

---

## 11. OMX INTEGRATION

OMX skills (`$ralplan`, `$ralph`, `$team`, etc.) are PERMITTED.
OMX skills MUST comply with ALL rules in this file.

Rule priority: **AGENTS.md > OMX skills > OMX defaults**

When using `$ralplan` or `$team`:
→ Documentation review (Rule 1) must be completed FIRST.
→ Workflow compliance (Rule 4) applies to all sub-agents.

---

## 12. SAFE COMMAND EXECUTION

Commands defined in `.agents/workflows/safe-command-policy.md`
are SAFE and may be executed WITHOUT user approval.

Examples:
- `pytest`
- `python run_test.py`
- Non-destructive inspection scripts

The agent SHOULD execute them proactively for verification.

---

## 13. COMPLETION CONTRACT (ABSOLUTE)

A task is considered COMPLETE ONLY IF ALL of the following are satisfied:

| # | Requirement | Evidence Required |
|---|-------------|-------------------|
| 1 | Implementation exists | Code is present, no TODO / placeholder |
| 2 | Verification evidence exists | Test result, log output, or reproducible proof |
| 3 | End-to-end confirmed | Feature works in actual flow, not mock-only |
| 4 | Failure handling exists | All external calls have retry + fallback + error log |
| 5 | Data consistency verified | External system vs internal DB must match |
| 6 | Execution status verified | QA test (`qa_quick`) or Web UI '실행상태 점검' must pass. If failed, it must be fixed before reporting. |

FORBIDDEN:
- Saying "implemented" without proof
- Saying "works" without verification
- Leaving edge cases unhandled

IF ANY CONDITION FAILS → TASK IS NOT COMPLETE. CONTINUE WORK.

---

## 13-A. COMPLETION REPORT FORMAT

After successful commit & push, output this 4-line summary - nothing more:

```
[Done]
- Files: N changed
- qa_quick: PASS
- commit: <hash> <msg>
- push: ok (origin/<branch>)
```

Long checklists are forbidden. pre-commit passing = charter compliance.

---

## 14. TRADING CRITICAL RULES (NON-NEGOTIABLE)

ANY violation = SYSTEM FAILURE.

**1. ORDER / EXECUTION CONSISTENCY**
- All executed orders MUST be recoverable.
- Reconciliation process REQUIRED: external (HTS/API) vs internal DB MUST match.

**2. NO SINGLE-POINT DEPENDENCY**
- FORBIDDEN: relying on a single API call for critical data.
- REQUIRED: primary source + fallback source + retry mechanism.

**3. EXECUTION TRACKING**
Each order MUST have:
- Intent record (PENDING)
- Execution record (broker response)
- Final state (FILLED / FAILED / CANCELLED)
NO EXCEPTIONS.

**4. FAILURE VISIBILITY**
ALL failures MUST be: logged, traceable, alertable.
Silent failure = CRITICAL ERROR.

**5. POLLING LIMITATION RULE**
Polling-only systems are NOT reliable.
If polling is used: must include retry + reconciliation.
Must NOT be sole source of truth.

---

## 14-A. FINANCIAL SYSTEM & DEVELOPMENT RULES

#### 5.1 모든 주문은 멱등성 키를 가진다 [MUST]
```python
# 같은 시그널에 대해 재시도해도 중복 주문 발생 X
order_key = generate_order_key(signal)  # 결정적 해시
idempotency_guard.execute_once(order_key, lambda: execute_order(signal))
```

#### 5.2 상태 변경은 반드시 Audit Log를 남긴다 [MUST]
- 모든 포지션 변경
- 모든 주문 요청/응답
- 모든 설정 변경
- 모든 시스템 상태 전환 (Circuit Breaker, Kill Switch 등)

```python
with journal.trace(signal) as trace:
    result = executor.execute(signal)
    trace.record(result)
```

#### 5.3 Circuit Breaker를 우회하는 코드 금지 [MUST]
- 모든 외부 브로커 호출은 Circuit Breaker 경유
- "이 한 번만..."은 금지

#### 5.4 새 전략/매매 로직은 Shadow Mode 선행 [MUST]
- 실거래 전 최소 1주일 Shadow 실행
- Shadow와 실거래 편차 임계치 초과 시 롤백

#### 5.5 Kill Switch 상태 체크 [MUST]
- 모든 주문 실행 진입점에서 Kill Switch 확인
- Kill Switch 활성 시 즉시 거부

```python
def execute(self, signal):
    if KillSwitch.is_active():
        raise SystemHaltedError("Kill Switch is active")
    ...
```

---

### § 6. 변경 관리 규칙

#### 6.1 Feature Flag로 감싼다 [MUST]
새 로직, 실험적 변경은 Feature Flag 뒤에 둔다.

```python
if flags.use_new_risk_model:
    risk = NewRiskManager()
else:
    risk = LegacyRiskManager()  # 기존 안정 버전 항상 유지
```

#### 6.2 마이그레이션은 양방향 [MUST]
DB 스키마 변경, 설정 변경 등은 **forward + rollback** 둘 다 작성.

#### 6.3 브랜치 전략 [MUST]
- `main` — 실거래 안정 버전 (직접 push 금지)
- `develop` — 통합 개발
- `feature/*` — 기능 개발
- `hotfix/*` — 긴급 수정 (main으로 직행 가능, 단 사후 회고 필수)

#### 6.4 PR 규칙 [MUST]
모든 PR은 다음을 포함:
- [ ] 변경 목적 설명
- [ ] 관련 이슈 링크
- [ ] 테스트 추가/변경 내역
- [ ] 배포 영향 분석 (실거래 중단 필요 여부)
- [ ] 롤백 방법
- [ ] 리스크 및 대응

---

### § 7. 코드 스타일

#### 7.1 Ruff 포맷터/린터 [MUST]
- `ruff check` 및 `ruff format` 통과 필수
- 설정: `pyproject.toml`의 `[tool.ruff]`

#### 7.2 네이밍 [MUST]
- 변수/함수: `snake_case`
- 클래스: `PascalCase`
- 상수: `UPPER_SNAKE_CASE`
- 사적 멤버: `_leading_underscore`
- 매직 넘버 금지 — 상수로 추출

#### 7.3 주석 [SHOULD]
- **"무엇"이 아닌 "왜"를 설명**
- 함수 docstring: 목적, 파라미터, 반환, 발생 예외 명시
- 복잡한 금융 로직은 반드시 주석 (예: 수수료 계산, 스왑 처리)

---

### § 8. 문서화 규칙

#### 8.1 코드와 함께 문서 업데이트 [MUST]
- API 변경 시 관련 문서 동시 수정
- `ARCHITECTURE.md`, `RUNBOOK.md` 등

#### 8.2 결정 기록 (ADR) [SHOULD]
중요한 설계 결정은 `docs/adr/NNNN-title.md`에 기록:
- 배경 (Context)
- 결정 (Decision)
- 결과 (Consequences)
- 대안 (Alternatives considered)

#### 8.3 포스트모템 [MUST]
프로덕션 장애 발생 시 24시간 내 `docs/postmortems/YYYYMMDD-title.md`:
- 타임라인
- 영향 범위 (금액 포함)
- 근본 원인
- 재발 방지책 (실행 가능한 작업 항목)


---

## 15. DEPLOY BLOCK RULE (ABSOLUTE)

DEPLOYMENT MUST BE BLOCKED IF:
- Verification is missing
- Reconciliation is missing
- Failure handling is missing
- Logs are not produced
- Data mismatch is possible

"Partial implementation" MUST NOT be deployed. NO EXCEPTIONS.

---

## 16. TASK DEFINITION RULE (MANDATORY)

Every task MUST include ALL of the following before starting:

1. PROBLEM — 무엇이 문제인가
2. ROOT CAUSE — 원인 또는 가설
3. REQUIRED CHANGES — 변경 범위
4. COMPLETION CRITERIA — 완료 기준
5. VERIFICATION METHOD — 검증 방법

If any is missing → TASK IS INVALID → DO NOT START.

---

## 17. ENCODING SAFETY RULE (MANDATORY)

All text-based source/config/doc files MUST use UTF-8 without BOM.

Before modifying any text file:
1. Detect current file encoding.
2. Preserve UTF-8 encoding throughout.
3. Do NOT rewrite file with a different encoding.
4. Do NOT introduce BOM characters.


---

## 18. AI SPECIAL DIRECTIVES

### AI-1. 불확실할 때는 중단한다 [MUST]
확신이 없는 변경은 코드를 작성하지 말고 **질문**한다.
특히 금융 로직(진입가, 손절, 수량 계산)은 100% 확실하지 않으면 중단.

### AI-2. 기존 테스트를 임의로 삭제/비활성화 금지 [MUST]
테스트가 실패하면 원인을 분석한다. 테스트를 끄지 않는다.

### AI-3. 대규모 리팩토링 전 설계 제시 [MUST]
10개 이상의 파일을 건드리는 변경은 먼저 설계안을 제시하고 승인을 받는다.

### AI-4. 컨텍스트 유실 시 재확인 [MUST]
긴 대화 중 이전 결정을 잊은 것 같으면 **물어보고 재확인**한다.
추측으로 이어가지 않는다.

### AI-5. "작동하는 것 같다"는 완료가 아니다 [MUST]
- 테스트 실행 결과 확인
- Pyright 통과 확인
- 실제 통합 확인
위 3개가 모두 확인된 후에만 "완료" 보고한다.

### AI-6. 외부 API 스펙은 추측하지 않는다 [MUST]
MT5, KIS, Upbit 등의 응답 형식을 **모른다면**:
1. 공식 문서 링크 요청
2. 실제 응답 샘플 요청
3. Contract Test로 스펙 고정


---

## 19. HARD BANS (STRICTLY FORBIDDEN)

아래는 **어떤 이유로도 허용되지 않는다**:

1. ❌ `except Exception: pass` — 침묵 실패 금지
2. ❌ 타입 힌트 없는 public 함수
3. ❌ 외부 API 응답을 dict로 내부 전파
4. ❌ 테스트 없이 merge
5. ❌ Feature Flag 없이 실거래 로직 배포
6. ❌ Kill Switch / Circuit Breaker 우회
7. ❌ Audit Log 없는 상태 변경
8. ❌ 하드코딩된 시크릿 (API 키, 비밀번호)
9. ❌ `main` 브랜치 직접 push (hotfix 제외, 사후 회고 필수)
10. ❌ "임시로" 주석 처리된 테스트 (반드시 이슈 링크 + 복구 기한)
