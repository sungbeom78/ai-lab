# 01. 실행 규칙

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)

---

## ★ 절대 규칙

> 모든 시스템 실행은 `run.py` 하나로 통일한다.
> 모든 테스트 실행은 `run_test.py` 하나로 통일한다.
> 이 외의 파일을 실행 진입점으로 만드는 것은 금지한다.

---

## 1. 시스템 실행 — `run.py`

```bash
python run.py [option] [program]
```

| 인자 | 값 예시 |
|------|---------|
| `option` | `start` / `stop` / `status` / `restart` |
| `program` | `kr_stock` / `us_stock` / `fx_fut` / `crypto` |

- `program`에 대응하는 전략 흐름은 `config/trade/{program}.trade.yaml`에서 로드한다.
- `.bat`, `.sh`는 Python 실행을 호출하는 보조 용도로만 사용한다. 직접 실행 로직 금지.

## 2. 테스트 실행 — `run_test.py`

```bash
python run_test.py [기능명칭] [옵션] [인자값1,인자값2,...]
```

- 테스트 전용 라이브러리는 `lib_test/`에서 관리한다.
- `lib_test/`와 테스트 코드는 Git으로 관리한다.

## 3. 금지 사항

- `src/` 내부 모듈을 직접 실행하는 것 금지.
  (`python src/adapter/kr/kis_adapter.py` 형태 금지)
- 내부 모듈에 `if __name__ == "__main__":` 독립 실행 블록 추가 금지.
  디버그 목적이라면 `script/operation/`에 별도 스크립트 작성.
