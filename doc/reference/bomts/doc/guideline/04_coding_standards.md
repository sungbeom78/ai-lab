# 04. 코딩 표준 (ts 프로젝트)

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)
> 전역 코딩 표준 (PEP8, 타입 힌트, f-string, `^` 줄바꿈, 결정론): **GEMINI.md RULE 7 / RULE 8**

---

## 이 문서의 범위

GEMINI.md에서 정의한 전역 코딩 표준 외에,
ts 프로젝트에만 적용되는 추가 규칙을 정의한다.

---

## 1. 예외 처리 — execution / risk 경로

```python
# ✅ execution / risk 경로 — 예외를 반드시 기록하고 재발생시킨다
try:
    result = execute_order(intent)
except Exception as e:
    logger.error(
        "order_execute_failed",
        extra={"intent": intent.dict(), "error": str(e)}
    )
    raise  # 예외를 삼키지 않는다

# ❌ 금지
try:
    result = execute_order(intent)
except Exception:
    pass
```

---

## 2. 구조화 로깅 필수 항목

아래 이벤트는 반드시 구조화된 형태로 로깅해야 한다.

| 이벤트 | 필수 포함 필드 |
|--------|----------------|
| signal 발생 | `market`, `symbol`, `direction`, `score`, `timestamp` |
| order_intent 생성 | `market`, `symbol`, `side`, `qty`, `price`, `intent_id` |
| broker_response 수신 | `intent_id`, `order_no`, `status`, `timestamp` |
| fill 체결 | `order_no`, `fill_price`, `fill_qty`, `timestamp` |

---

## 3. 식별자 네이밍 — ts 프로젝트 추가 규칙

전역 네이밍 컨벤션(GEMINI.md RULE 8-2) 외에 ts 프로젝트는
`glossary/terms.json`의 약어를 식별자 기준으로 사용한다.

상세 규칙: [06_glossary_rules.md](06_glossary_rules.md)
