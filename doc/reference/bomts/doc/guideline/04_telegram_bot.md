# 04. 텔레그램 봇 운영 구조 지침

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)

---

## 1. 기본 원칙

텔레그램 봇은 총 3종류로 운영한다.

| 봇 이름 | 역할 | 환경변수 (토큰) |
|---------|------|----------------|
| ts zero system | 시스템 전체 관제 | `TELEGRAM_SYSTEM_TOKEN` |
| ts zero test | 테스트 실행/결과 알림 | `TELEGRAM_TRADE_TEST_TOKEN` |
| ts zero market kr | KR 시장 운영/거래 알림 | `TELEGRAM_KR_TRADE_TOKEN` |
| ts zero market fx | FX 시장 운영/거래 알림 | `TELEGRAM_FX_TRADE_TOKEN` |
| ts zero market us | US 시장 운영/거래 알림 | `TELEGRAM_US_TRADE_TOKEN` |
| ts zero market crypto | Crypto 시장 운영/거래 알림 | `TELEGRAM_CRYPTO_TRADE_TOKEN` |

**권한 계층:**
- system 봇: 최고 권한 (전체 제어 가능)
- test 봇: 테스트 전용 (운영 제어 금지)
- market 봇: 자기 시장 범위 내에서만 제어 가능

---

## 2. 봇별 역할

### 2-1. ts zero system

**역할:** 전체 시스템 관리, 전체 서비스 시작/중지, 공통 상태 조회, 장애/하트비트 수신

**수신 메시지 유형:**
- `[STARTUP]` / `[SHUTDOWN]` — 시스템 시작/종료
- `[HEARTBEAT]` — 주기적 생존 신호
- `[ALERT]` — 장애/경고
- `[SNAPSHOT]` — 전체 스냅샷 결과
- `[SCHEDULER]` — 스케줄러 작업 결과

**허용 명령:**

```
/help, /status, /health
/start all, /stop all, /restart all
/snapshot, /snapshot all
/report today, /report week, /report month
/halt all, /resume all
```

> `/start all`, `/stop all`, `/restart all` 은 **system 봇에서만** 허용

---

### 2-2. ts zero test

**역할:** run_test.py 기반 테스트 실행 결과 발송, 개발/검증 알림 전용

**수신 메시지 유형:**
- `[TEST START]` / `[TEST SUCCESS]` / `[TEST FAIL]`
- 수행 라이브러리명, 함수명, 파라미터, 결과 요약, 소요시간

**발송 문구 기본 형식:**
```
[TEST START]
테스트작업 수행 : strategy.kr.selector
function=run_selector_test
time=2026-03-22 13:00:00
```

**허용 명령:**

```
/help, /status, /health, /snapshot
/test list, /test run [대상], /test stop, /test result, /test logs
/report test
```

> 실거래 시작/중지, `/start all`, `/stop all` 금지

---

### 2-3. ts zero market [시장명]

**역할:** 해당 시장 서비스 운영, 거래/전략/리스크 알림

**지원 시장:** `kr` | `fx` | `us` | `crypto`

**수신 메시지 유형:**
- `[MARKET START]` / `[MARKET STOP]`
- `[SIGNAL]` — 전략 신호 발생
- `[ORDER]` / `[FILL]` — 주문 접수/체결
- `[EXIT]` — 청산 (reason, pnl 포함)
- `[RISK]` — 리스크 이벤트 (일손 제한, 신규진입 중단 등)
- `[SNAPSHOT]` — 시장별 스냅샷

**허용 명령:**

```
/help, /status, /health, /snapshot
/start, /stop, /restart
/positions, /orders, /pnl, /risk
/halt, /resume
```

**선택적 허용 (운영 안정화 후 활성화):**

```
/buy [종목] [수량]
/sell [종목] [수량]
/flatten
/cancel_all
```

> `/start`, `/stop` 은 자기 시장 서비스에만 적용 — 전체/타 시장 제어 불가

---

## 3. 공통(common) 기능

모든 봇에서 재사용하는 공통 계층.

| 기능 | 설명 |
|------|------|
| 명령 파싱 | 커맨드 + 인자 분리 |
| 권한 검증 | chat_id / user_id 기반 거부 |
| 응답 포맷터 | 통일된 응답 형식 |
| 에러 핸들링 | 예외 → 표준 에러 메시지 |
| 로그 기록 | bot_name, chat_id, command, result, timestamp |
| 하트비트 발송 | system 봇 전달 |
| 상태/스냅샷/리포트 포맷 | 공통 출력 형식 |

**공통 응답 상태 코드:**

```
ACCEPTED / STARTED / SUCCESS / FAILED / REJECTED / NOT_ALLOWED / INVALID_COMMAND / NOT_IMPLEMENTED
```

**공통 응답 형식:**

```
[STATUS] SUCCESS
bot: ts zero market kr
command: /start
target: KR
time: 2026-03-22 15:00:00
message: KR market service started
```

**공통 에러 형식:**

```
[ERROR] REJECTED
bot: ts zero test
command: /start all
reason: command not allowed in test bot
```

---

## 4. 구현 구조

```
src/telegram/
├── common/
│   ├── formatter.py          # ResponseFormatter
│   ├── auth.py               # 권한 검증 (chat_id / user_id)
│   ├── command_registry.py   # CommandRegistry (명령 → 핸들러 매핑)
│   └── notification.py       # NotificationService (메시지 템플릿)
├── system/
│   └── system_bot.py         # ts zero system 핸들러
├── test/
│   └── test_bot.py           # ts zero test 핸들러
└── market/
    ├── base_market_bot.py    # market 봇 공통 핸들러
    ├── kr_bot.py
    ├── fx_bot.py
    ├── us_bot.py
    └── crypto_bot.py
```

**BotRouter:** `bot_type = system | test | market` + `market = kr | us | fx | crypto | null`

**로그 필수 항목:** `bot_name`, `chat_id`, `user_id`, `command`, `arguments`, `result`, `timestamp`

**민감 명령 2단계 보호 대상:**
- `/stop all`, `/restart all`, `/flatten`, `/buy`, `/sell`

---

## 5. 명령 허용 범위 요약

| 명령 | system | test | market |
|------|--------|------|--------|
| /start all / /stop all | ✅ | ❌ | ❌ |
| /start / /stop (자기 시장) | ✅ | ❌ | ✅ |
| /snapshot | ✅ | ✅ | ✅ |
| /report | ✅ | test만 | ✅ |
| /test run | ❌ | ✅ | ❌ |
| /buy / /sell | ❌ 권장 | ❌ | ✅ 제한적 |
| /flatten | ✅ | ❌ | ✅ |
| /halt all | ✅ | ❌ | ❌ |
| /halt (자기 시장) | ✅ | ❌ | ✅ |

---

## 6. 핵심 요약

- **ts zero system** : 전체 시스템 운영/관제 봇
- **ts zero test** : 테스트 작업 실행/결과 알림 봇
- **ts zero market** : 시장별 운영/거래 알림 봇
- **common** : 모든 봇이 공유하는 공통 기능 계층
- 전체 제어는 system 전용
- 시장 제어는 market 전용
- 테스트 제어는 test 전용
- 명령/응답/로그/권한은 표준화
- 구조는 단순하게, 책임은 명확하게
