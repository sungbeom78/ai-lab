# 02. 설정 관리 규칙

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)
> 관련 전역 규칙: GEMINI.md RULE 6

---

## ★ 절대 규칙

> 민감정보는 `.env`에만.
> 파라미터는 `settings.yaml`에만.
> 전략 흐름은 `trade/*.yaml`에만.
> 소스 코드 하드코딩 절대 금지. (GEMINI.md RULE 6)

---

## 1. 설정 파일 역할 분리

| 파일 | 저장 대상 | Git |
|------|-----------|-----|
| `.env` | 계정, 비밀번호, API Key/Secret, 서버 주소, 경로 | ❌ 제외 |
| `.env.example` | `.env` 키 목록 (값 없음) | ✅ 포함 |
| `config/settings.yaml` | 손절·익절 비율, 필터 기준, 알림 옵션 등 파라미터 | ❌ 제외 |
| `config/settings.example.yaml` | `settings.yaml` 구조 예시 | ✅ 포함 |
| `config/trade/{market}.trade.yaml` | 마켓별 전략 흐름, 작업 순서, 호출 클래스 목록 | ✅ 포함 |

---

## 2. `.env` 관리 항목

```ini
# 계정
KIS_ACCT=
KIS_AK=
KIS_AS=
KIS_MAK=
KIS_MOCK=

# 인프라
PG_DSN=
REDIS_URL=
MT5P=
E_FX=
E_KR=
E_US=
E_CRYPTO=

# 시스템
NODE_NAME=
DASH_P=
PROJECT_ROOT=

# AI
GOOGLE_API_KEY_OCR=
GOOGLE_API_KEY_EVAL=
ANTHROPIC_API_KEY=
OPENAI_API_KEY=

# 알림
TELEGRAM_BOT_TOKEN=
TELEGRAM_CHAT_ID=
```

> 환경변수명은 `glossary/terms.json`의 `abbr_short` 기준.
> 상세: [06_glossary_rules.md](06_glossary_rules.md)

---

## 3. `config/settings.yaml` 관리 항목

민감정보를 제외한 파라미터만 관리한다.

```yaml
system:
  # 시스템 운영 설정

sessions:
  kr_stock:
    market_open:    "09:00"
    market_close:   "15:30"
    no_entry_after: "15:00"

kr_strategy:
  stop_loss_rate:   0.02
  take_profit_rate: 0.05

scoring:
  momentum_weight:  0.4
  volume_weight:    0.3

backtest:
  start_date: "2024-01-01"

reporting:
  daily_report: true
```

---

## 4. `config/trade/{market}.trade.yaml` 관리 항목

마켓별 전략 실행 흐름을 정의한다. 파라미터 값은 포함하지 않는다.

```yaml
# config/trade/kr_stock.trade.yaml
market: kr_stock
steps:
  - name: collect_market_data
    class: collectors.KrStockCollector
  - name: select_leaders
    class: selector.SectorRanker
  - name: generate_signals
    class: signals.KrSignalEngine
  - name: manage_risk
    class: risk.RiskManager
  - name: execute_orders
    class: execution.ExecutionEngine
```

---

## 5. 코드에서 설정값 로드

```python
# ✅ .env 값
import os
from dotenv import load_dotenv
load_dotenv()
app_key = os.getenv("KIS_AK")

# ✅ settings.yaml 값
from src.common.config import Settings
cfg = Settings.get_instance()
stop_loss = cfg.kr_strategy.stop_loss_rate

# ✅ 경로 조합
from pathlib import Path
base = Path(os.getenv("PROJECT_ROOT"))
cookie_path = base / "config" / "cookies"

# ❌ 금지
app_key     = "PSPi5fd..."
db_host     = "192.168.1.100"
cookie_path = Path("C:/project/ts/config/cookies")
```
