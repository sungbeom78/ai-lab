# Source of Truth (SoT) 선언표 — BOM_TS

> 시스템 내 **모든 데이터/설정/상태의 유일한 정의 위치**를 명시합니다.
> 이 표에 명시된 소유 모듈 외에서는 해당 데이터를 **생성/수정/삭제할 수 없습니다**.

---

## 1. 도메인 모델 SoT

> 모든 도메인 모델은 `src/common/models.py`에서만 정의한다.

| 모델 | SoT 위치 | 수정 권한 | 금지사항 |
|------|---------|---------|---------|
| `Market`, `Bar`, `Tick` | `src/common/models.py` | 승인 필요 | 다른 모듈에서 dict로 우회 금지 |
| `SectorScore`, `StockScore` | `src/common/models.py` | 승인 필요 | selector 외 모듈에서 재계산 금지 |
| `SignalEvent` | `src/common/models.py` | 승인 필요 | signals 외 모듈에서 생성 금지 |
| `OrderIntent`, `Order`, `Fill` | `src/common/models.py` | 승인 필요 | execution 외 모듈에서 생성 금지 |
| `Position` | `src/common/models.py` | 승인 필요 | 다른 모듈 재계산 금지 |
| `AccountSnapshot` | `src/common/models.py` | 승인 필요 | dashboard 직접 조회 금지 |

> [!CAUTION]
> 브로커 응답 원본(dict/JSON)을 내부 모델처럼 사용 금지.
> 반드시 `models.py`의 정의된 모델로 변환 후 사용.

---

## 2. 설정 SoT

| 대상 | SoT 위치 | 수정 권한 | 금지사항 |
|------|---------|---------|---------|
| 민감정보 (API 키, DB 접속) | `.env` | 제한 | 코드 하드코딩 금지 |
| 튜닝 파라미터 (threshold, weight) | `config/settings.yaml` | 제한 | 코드 내 기본값 금지 |
| 마켓별 전략 설정 | `config/trade/*.trade.yaml` | 제한 | 다른 파일에 분산 금지 |
| 설정 키 이름 | `settings.yaml` 기존 키 | 잠금 | 임의 이름 변경 금지 |

> [!IMPORTANT]
> settings.yaml의 **기존 키 이름**은 고정값. 새 키 추가는 가능하되 기존 키 변경은 승인 필수.

---

## 3. 데이터 소유권 SoT

| 데이터 | 소유 모듈 (쓰기) | Authoritative Source | 저장 위치 |
|--------|----------------|---------------------|----------|
| 당일 거래 이벤트 | `execution/orchestrator` | `today_trading_by_market` | 메모리 + data/journal/ + DB |
| 계좌 상태 | `execution/orchestrator` | `account_by_market` | 메모리 (브로커 API 갱신) |
| 종목 메타 | `selector` + `orchestrator` | `symbol_index_by_market` | 메모리 |
| 파이프라인 흐름 | `selector` + `signals` | `pipeline_by_market` | 메모리 |
| 호가 스냅샷 | `collectors/orderbook_collector` | Redis `orderbook:snapshots` | Redis → DB |
| 시그널 판단 | `signals/*_engine` | 반환값 (저장 안 함) | — |
| 거래 이력 (감사) | `execution/trade_journal` | journal 파일 + DB | data/journal/ + DB |

> 이 표는 `09_data_flow.md`와 동기화됩니다.

---

## 4. 저장소 역할 SoT

| 저장소 | 역할 | 성격 |
|--------|------|------|
| 4개 authoritative dict | 런타임 기준 데이터 | **Authoritative** — 런타임 진실 |
| PostgreSQL | System of Record | **Authoritative** — 영구 진실 |
| Redis | 실시간 캐시 + 이벤트 스트림 + 호가 버퍼 | Derived — DB가 원본 |
| data/journal/ | 거래 JSON 파일 | Supplementary — 저장/복구/감사용 |
| json 캐시 (kr_status 등) | 임시 저장 / 외부 전달 | Derived — 집계 소스 아님 |

> [!WARNING]
> **런타임 집계는 4개 authoritative dict에서만 수행한다.**
> journal / DB / json 캐시를 런타임 집계 소스로 사용하면 안 된다.
> session_summary는 제거 대상이며, 모든 집계는 raw list에서 직접 계산한다.

---

## 5. 문서 SoT

| 문서 | 역할 | 수정 시점 |
|------|------|----------|
| `doc/README_AI_GUIDELINE.md` | AI 작업 제한 기준 | 구조 변경 시 |
| `doc/module_index.md` | 모듈 네비게이션 + 책임 경계 | 모듈 추가/변경 시 |
| `doc/guideline/09_data_flow.md` | 데이터 흐름 규칙 + 불변 조건 | 데이터 경로 변경 시 |
| `doc/SOURCE_OF_TRUTH.md` | SoT 선언표 (이 파일) | 소유권 변경 시 |
| `doc/change_log.md` | 변경 이력 | 모든 비사소한 변경 후 |

---

## 6. 인터페이스 잠금 (Frozen Interfaces)

> 아래 항목은 **사용자 승인 없이 수정 불가**.

| 대상 | 파일 | 이유 |
|------|------|------|
| 도메인 모델 공개 필드 | `src/common/models.py` | 전체 시스템 호환성 |
| 설정 키 이름 | `config/settings.yaml` | 런타임 호환성 |
| DB 스키마 기존 컬럼 | `script/db/schema*.sql` | 데이터 정합성 |
| 브로커 어댑터 공개 인터페이스 | `src/adapter/*/base.py` | 브로커 연동 안정성 |
| Redis 키 패턴 | `src/storage/redis_client.py` | 다중 소비자 호환 |

---

## 변경 절차

이 문서의 내용을 변경해야 할 때:

1. 변경 사유와 영향 범위를 먼저 명시
2. 사용자 승인 획득
3. 관련 코드와 문서 동시 수정
4. `doc/change_log.md`에 기록
