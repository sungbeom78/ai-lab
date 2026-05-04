# 09. 데이터 흐름 규칙

> BOM_TS 시스템에서 데이터가 어디서 생성되고, 누가 소유하며, 어떻게 읽혀야 하는지 정의한다.
> 모든 코드 변경 전 이 문서를 확인한다.

---

## 1. 레이어 규칙

```text
adapters/   broker API 연동 (KIS, MT5, Upbit)
execution/  adapter 사용 + runtime 상태 통합 + 주문 실행
report/     execution 상태 읽기 전용
```

### 허용/금지 매트릭스

| 읽는 쪽 | adapters/ | collectors/ | signals/ | execution/ | report/ |
|--------|:---------:|:-----------:|:--------:|:----------:|:-------:|
| adapters/ | - | X | X | X | X |
| collectors/ | O | - | X | X | X |
| signals/ | O | O | - | X | X |
| execution/ | O | O | O | - | X |
| report/ | X | X | X | O | - |

> [!CAUTION]
> `report/`에서 `adapters/`를 직접 호출하지 않는다.

---

## 2. 데이터 소유권

각 데이터에는 **소유 모듈(Owner)** 이 하나만 존재한다.
소유 모듈만 해당 데이터를 생성/수정/삭제할 수 있고, 다른 모듈은 읽기만 허용된다.

| 데이터 | 소유 모듈 | 입력 원천 | 읽기 허용 | 저장 위치 | 금지 사항 |
|--------|----------|----------|----------|----------|---------|
| 거래 현재 상태 (보유 종목/주문/당일 체결) | `execution/orchestrator` | fills, broker sync, execution events | report/, signals/ | `today_trading_by_market` | 별도 summary/current-state dict 생성 금지 |
| 계좌 상태 | `execution/orchestrator` | broker API (adapters 경유) | report/ | `account_by_market` | dashboard 직접 API 호출 금지 |
| 종목 메타 | `selector` + `execution/orchestrator` | selector, execution events | report/, signals/ | `symbol_index_by_market` | 화면/리포트용 별도 symbol cache 생성 금지 |
| 파이프라인 상태 | `selector` + `signals` | scan/filter/score/rank 결과 | execution/, report/ | `pipeline_by_market` | stage 순서 하드코딩 금지 |
| 호가 스냅샷 | `storage/orderbook_repo` | KIS API (collectors 경유) | signals/, report/ | DB kr_orderbook_snapshot | dashboard 직접 API 호출 금지 |
| 시그널 판단 | `signals/*_engine` | bars, selector 결과 | execution/ | 반환값(비영구) | execution에서 재판단 금지 |
| 거래 이력 (감사/복구) | `execution/trade_journal` | orders, fills | execution/ | data/journal/ + DB | 실시간 집계 source로 직접 사용 금지 |
| 리스크 이벤트 | `risk/*_manager` | 포지션 + 설정값 | execution/, report/ | DB risk_events | signals에서 자체 차단 금지 |

> SoT 통합 선언: [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md)

---

## 3. 불변 규칙 (Invariants)

### 보유 종목

- **INV-001**: 시스템이 인식하는 현재 보유 종목 전체 = `today_trading_by_market[market]["open_positions"]`
- **INV-002**: 대시보드 "활성 거래/보유 종목" 표시는 `today_trading_by_market` 현재 상태 기준으로 구성한다
- **INV-003**: 시스템 시작 시 브로커/저널 복구가 완료되면 orchestrator가 현재 상태를 4개 dict에 동기화한다
- **INV-004**: 신규 진입 제한(`max_open_positions`)과 중복 진입 차단은 `today_trading_by_market.open_positions` + `today_trading_by_market.orders` 기준으로 계산한다
- **INV-005**: 현재 보유 종목 수가 `max_open_positions`를 초과하면, orchestrator는 평가 시점의 미실현손익 기준으로 손실이 가장 큰 종목부터 제한 이내가 될 때까지 즉시 청산을 시도한다

### 데이터 흐름

- **INV-010**: 외부 API(KIS/Upbit/MT5)는 `adapters/`에서만 호출한다
- **INV-011**: `report/`는 `execution/` 상태만 읽는다. `adapters/` 직접 호출 금지
- **INV-012**: 대시보드/리포트 표시용 계산 결과는 execution이 계산하고 report는 읽기만 한다

### 기능 추가

- **INV-020**: 새로운 거래 관련 데이터가 필요하면 먼저 4개 authoritative dict 중 어디에 속하는지 판단한다
- **INV-021**: 거래 관련 데이터 접근은 `today_trading_by_market`, `account_by_market`, `symbol_index_by_market`, `pipeline_by_market` 기준으로 한다
- **INV-022**: `TradeJournal`, journal file, DB, json cache는 복구/감사/영속화 용도이며 현재 상태 집계의 기준으로 직접 사용하지 않는다

---

## 4. 기능 추가 시 체크리스트

```text
새 기능이 현재 상태인지, 감사/복구 데이터인지 먼저 구분했는가?
4개 authoritative dict 중 어디에 들어가야 하는지 먼저 판단했는가?
report가 execution 상태만 읽고 있는가?
position limit / duplicate entry / summary 계산이 현재 상태 dict 기준인가?
관련 테스트가 변경 범위를 커버하는가?
```

---

## 5. 위반 사례와 교훈

### 사례: KR 보유 종목 표시 (2026-03-24)

| 경로 | 문제 |
|------|------|
| dashboard | broker API 직접 호출로 보유 종목 표시 |
| trading engine | 별도 기준으로 활성 종목 판단 |

**교훈**: 통합 관점에서는 "현재 거래 상태의 authoritative source = 4개 market dict"를 먼저 확인해야 한다. `TradeJournal`은 체결/복구/감사용 기록과 실행 보조 역할을 맡고, 대시보드와 진입 제한 판단은 `today_trading_by_market` 현재 상태를 기준으로 읽어야 한다.
