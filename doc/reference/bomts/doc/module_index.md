# Module Index ??BOM_TS

> ?쒖뒪???대퉬寃뚯씠??留? 媛?紐⑤뱢??寃쎈줈, ?대옒?? ??븷, 吏꾩엯?먯쓣 湲곕줉?쒕떎.

---

> 2026-04-11 update: PMR/GoldenKey/Admin/StockClassifier SQL read paths now resolve `stock`/`theme`/`leader_stock` via `src/storage/table_contract.py` for singular table compatibility.
> 2026-04-11 update: `routes/common_api.py` now serves both `/api/trades/closed` and `/admin/api/trades/closed` via `api_closed`; `script/operation/check_runtime.py` now uses only recent execution snapshots for DB-vs-execution checks.
> 2026-04-11 update: Windows MT5 handler path policy is unified to singular root `C:\project\bomts_mt5_handler` (no `C:\projects\...`), reflected in `.env.mt5_node.example` and migration guide archive docs.
> 2026-04-24 update: `run.py` FX path now enforces MT5 bridge client-only startup (`Mt5BridgeClient`) and blocks `NODE_ROLE=mt5_node` orchestrator execution; runtime MT5 local adapter path in launcher is decommissioned.
> 2026-04-24 update: `src/common/process_guard.py` now targets Python runtime processes only, preventing false-positive termination of PowerShell wrappers that include `run.py` markers in command text.
> 2026-04-30 update: market-per-process isolation — `status_aggregator.py` added; `runtime_status.json` direct read deprecated; `process_watchdog.py` rewritten with `WatchTarget` dataclass (per-market isolation); `startup_preflight.py` commands split per market (`trading_kr_stock`, `trading_fx_fut`).


## common
- Path: `src/common/`
- Classes: `Market`, `Bar`, `Tick`, `SectorScore`, `StockScore`, `SignalEvent`, `OrderIntent`, `Order`, `Fill`, `Position`, `AccountSnapshot`, `Settings`
- Responsibility: 怨듯넻 Pydantic 紐⑤뜽, ?ㅼ젙 濡쒕뜑, 援ъ“??濡쒓퉭, ?덉쇅 ?뺤쓽, ID ?좏떥, ?쒓컙 ?좏떥, ?꾨줈?몄뒪 媛??- Entry Point: `config.get_settings()`, `logging.get_logger()`
- Related Modules: 紐⑤뱺 紐⑤뱢?먯꽌 李몄“
- Config: `config/settings.yaml`

### Files
| File | Role |
|------|------|
| `models.py` | Pydantic v2 ?곗씠??紐⑤뜽 (Market, Bar, Tick, Order ?? |
| `config.py` | YAML + .env ?ㅼ젙 濡쒕뜑, Settings ?깃??? canonical MT5 bridge env alias (`MT5_BRIDGE_*` ??`MT5_PROXY_URL`) ?댁꽍, `TRADING_ENV` accessor ?쒓났 |
| `logging.py` | structlog 湲곕컲 援ъ“??濡쒓퉭 |
| `exceptions.py` | ??낅퀎 ?덉쇅 ?대옒??|
| `ids.py` | UUID ?ы띁 |
| `time_utils.py` | ?몄뀡/罹섎┛???쒓컙? ?좏떥, `is_active_day()` ?붿씪 ?쒖꽦 泥댄겕 |
| `process_guard.py` | 以묐났 ?꾨줈?몄뒪 諛⑹? |
| `runtime_bootstrap.py` | ?쒕퉬??紐⑤뱶/留덉폆 ?좏깮/QA startup 寃뚯씠??怨듯넻 ?댁꽍 |
| `service_manager.py` | 硫?곗꽌鍮꾩뒪 ?꾪궎?띿쿂 愿由?(DB/LOG/FX/KR/US/Crypto/Test) |
| `code_resolver.py` | 肄붾뱶 ???쒓뎅???쒖떆紐?蹂??(code_display ?뚯씠釉?罹먯떆) |
| `symbol_utils.py` | ?듯빀 醫낅ぉ紐?議고쉶 (resolve_symbol_name, format_symbol_display) ??KR:DB, FX:YAML(`data/symbol/fx_symbols.yaml`), CRYPTO:?댁옣 |
| `system_maintenance.py` | ?쇱씪 由щ????뺣━ ?쒖뒪??(?꾨줈?몄뒪/GC/濡쒓렇/?좏겙/諛깆뾽) |
| `backup.py` | 踰붿슜 諛깆뾽 留ㅻ땲? (settings.yaml > backup ?섏쐞 ?묒뾽 ?숈쟻 泥섎━, zip+?먭꺽+蹂댁〈) |
| `cookie_manager.py` | Playwright 荑좏궎 ????ъ궗??|
| `profiler.py` | py-spy 湲곕컲 ?깅뒫 ?꾨줈?뚯씪留?(settings.yaml > profiling, 二쇨린??flame graph+top ?앹꽦) |
| market_calendar.py | [NEW 2026-04-30] KrMarketCalendar singleton. KIS CTCA0903R for daily open/close (opnd_yn), 1-day cache, fail-open. refresh/is_close_day/reset methods. get_kr_market_calendar() factory. [NEW 2026-05-02] MarketSchedule batch cache: MarketStatus(OPEN/CLOSED/EARLY_HALT), MarketScheduleEntry, get_market_schedule() singleton. 7-day lookahead via exchange-calendars. build()/load()/get_status()/is_close_day()/get_entry_deny_time()/get_force_exit_time(). |

---

## risk
- Path: `src/risk/`
- Classes: `RiskManager`, `CryptoRiskManager`, `UsSwingRiskManager`
- Responsibility: 以묒븰 由ъ뒪???붿쭊 ???ъ????쒕룄, ?쇱씪 ?먯떎 ?쒗븳, ?ъ뒪?꾩튂 (?꾩껜 + 留덉폆蹂?, EOD 媛뺤젣 泥?궛
- Entry Point: `risk_manager.RiskManager()`, `kill_switch.is_active()`
- Related Modules: orchestrator, signal engines
- Config: `config/settings.yaml > risk`, `config/settings.yaml > risk_crypto`, `config/settings.yaml > risk_us_swing`

### Files
| File | Role |
|------|------|
| `kill_switch.py` | ?꾩껜/留덉폆蹂??ъ뒪?꾩튂 愿由?(tmp/kill.switch.*) |
| `risk_manager.py` | 以묒븰 由ъ뒪???붿쭊 (?ъ??? ?먯떎, P&L 異붿쟻, ?ъ뒪?꾩튂 ?곕룞) |
| `crypto_risk.py` | ?щ┰???꾩슜 由ъ뒪??(?곗냽 ?먯젅 李⑤떒, 醫낅ぉ ?ъ쭊???쒗븳) |
| `us_swing_risk.py` | US ?ㅼ쐷 ?꾩슜 由ъ뒪??(?뱁꽣 吏묒쨷 ?쒗븳, 珥??몄텧 ?쒕룄) |

---

## adapters
- Path: `src/adapter/`
- Classes: `MT5Bridge`, `MT5ProxyServer`, `KrBrokerStub`, `UsBrokerStub`, `UpbitAuth`, `UpbitAdapter`, `KisUsAdapter`
- Responsibility: ?몃? 釉뚮줈而??곕룞 ?대뙌??(MT5, KIS, US, Upbit)
- Entry Point: `base.py` ?명꽣?섏씠??- Related Modules: execution, collectors
- Config: `.env` (MT5_PROXY_URL, KIS_APP_KEY ??

### Files
| File | Role |
|------|------|
| `base.py` | ?대뙌???명꽣?섏씠???뺤쓽 |
| `mt5/proxy_server_win.py` | ?뵺 Windows MT5 bridge ?쒕쾭 (FastAPI, **?낅┰ ?꾨줈?몄뒪**). MT5 吏곷젹 ?몄텧, `/market/*`, `/order/*`, `/deploy`, auth token 泥섎━, deploy healthcheck ?몄쬆 ?ㅻ뜑(`DEPLOY_HEALTHCHECK_AUTH_TOKEN` ??`MT5_BRIDGE_AUTH_TOKEN`), `.env` ?먮룞 濡쒕뱶 諛?deploy ?ㅽ뙣 ??怨꾩빟 ?묐떟(JSON) 蹂댁옣 |
| `mt5/windows_bridge.py` | WSL/Linux ??Windows MT5 bridge ?대씪?댁뼵?? timeout/retry + circuit breaker + bearer auth ?ㅻ뜑 |
| `mt5/mt5_local_adapter.py` | 濡쒖뺄 MT5 ?대뙌??(BaseBrokerAdapter 援ы쁽, run.py ?듯빀?? `get_closed_deal_info(ticket)` deal history 議고쉶) |
| `kr/kis_auth.py` | KIS API ?몄쬆/?좏겙 愿由? `KisMockAuth` 紐⑥쓽?ъ옄 ?몄쬆 |
| `kr/kis_adapter.py` | KIS API ?대뙌??(?댁쨷 怨꾩쥖: ?ㅼ쟾 ?곗씠??+ 紐⑥쓽 留ㅻℓ, ?낆쥌 留덉뒪??議고쉶 異붽?, 泥닿껐 websocket怨??멸? websocket 而⑦뀓?ㅽ듃 遺꾨━, mock 嫄곕옒 ???멸? websocket? ?ㅼ떆??endpoint ?좎?) |
| `kr/kis_ws_client.py` | KIS KR 泥닿껐 websocket ?대씪?댁뼵??(execution notice, appkey collision backoff, reject control-frame preserve, health snapshot) |
| `kr/broker_stub.py` | ?쒓뎅二쇱떇 釉뚮줈而??ㅽ뀅 |
| `us/kis_us_adapter.py` | KIS API 誘멸뎅二쇱떇 ?대뙌??(?댁쨷怨꾩쥖: ?ㅼ쟾 ?곗씠??+ 紐⑥쓽 留ㅻℓ) |
| `us/__init__.py` | 誘멸뎅二쇱떇 ?대뙌???⑦궎吏 珥덇린??|
| `us/broker_stub.py` | 誘멸뎅二쇱떇 釉뚮줈而??ㅽ뀅 |
| `crypto/__init__.py` | ?뷀샇?뷀룓 ?대뙌???⑦궎吏 |
| `crypto/upbit_auth.py` | ?낅퉬??JWT ?몄쬆/?쒕챸 (PyJWT + SHA512) |
| `crypto/upbit_adapter.py` | ?낅퉬??REST API ?대뙌??(?붽퀬/罹붾뱾/二쇰Ц/?덉씠?몃━諛? |

---

## collectors
- Path: `src/collector/`
- Classes: `MT5Collector`, `OrderbookCollector`
- Responsibility: ?쒖옣 ?곗씠???섏쭛 (M1 諛? ??, ?멸? ?ㅻ깄???섏쭛 (1珥?二쇨린)
- Entry Point: `mt5_collector.py`, `orderbook_collector.py`
- Related Modules: adapters, storage
- Config: `settings.yaml > data`, `settings.yaml > kr_conditions`

### Forbidden
- ?꾨왂 ?먯닔 怨꾩궛 湲덉?
- 二쇰Ц ?먮떒/?앹꽦 湲덉?
- ?ъ????섏젙 湲덉?
- ?쒓렇???앹꽦 湲덉?

### Files
| File | Role |
|------|------|
| `mt5_collector.py` | MT5 遺꾨큺/???섏쭛 |
| `orderbook_collector.py` | ?멸? ?ㅻ깄???섏쭛 (1珥?二쇨린) ??Redis Stream 諛쒗뻾 (DB 吏곸젒 ?곌린 ?쒓굅) |
| `orderbook_consumer.py` | ?뵺 Redis Stream ??DB 諛곗튂 INSERT (5珥?二쇨린, **?낅┰ ?ㅽ뻾 媛??*) |
| `goldenkey_collector.py` | 怨⑤뱺???섏쭛湲?|
| `naver_premium_scraper.py` | ?ㅼ씠踰??꾨━誘몄뾼 ?μ쟾 由ы룷??OCR ?섏쭛 |

## selector
- Path: `src/selector/`
- Classes: `SectorRanker`, `SymbolRanker`, `MarketStrength`, `FxSymbolRanker`, `FxCandidateSelector`, `KrMarketScanner`
- Files: `sector_ranker_kr.py`, `symbol_ranker_kr.py`, `market_strength.py`, `fx_symbol_ranker.py`, `fx_candidate_selector.py`, `kr_scanner.py`
- Responsibility: ?뱁꽣 ??궧, 醫낅ぉ ??궧, ?쒖옣 媛뺣룄, KR ??μ＜ ?ㅼ틦??(議곌굔??湲곕컲 ?ы븿)
- Entry Point: `kr_scanner.py`, `sector_ranker_kr.py`
- Related Modules: signals, common, adapters
- Config: `settings.yaml > kr_selector`, `settings.yaml > market_strength`, `settings.yaml > kr_conditions`

### Forbidden
- 釉뚮줈而?API 吏곸젒 ?몄텧 湲덉? (adapters 寃쎌쑀 ?꾩닔)
- 二쇰Ц ?앹꽦/?꾩넚 湲덉?
- 由ъ뒪???뱀씤/李⑤떒 ?먮떒 湲덉?
- ?ъ????섏젙 湲덉?

### Files
| File | Role |
|------|------|
| `kr_scanner.py` | KR ??μ＜ ?ㅼ틦??(`scan()`, `scan_with_conditions()`) |
| `sector_ranker_kr.py` | ?뱁꽣 ??궧 |
| `symbol_ranker_kr.py` | 醫낅ぉ ??궧 |
| `market_strength.py` | ?쒖옣 媛뺣룄 |
| `fx_symbol_ranker.py` | ?뵺 FX 醫낅ぉ ??궧 (**?낅┰ ?ㅽ뻾**: `script/operation/select_fx_symbols.py` 寃쎌쑀) |
| `crypto_universe.py` | ?낅퉬??KRW 留덉폆 嫄곕옒?湲??곸쐞 N媛??좊땲踰꾩뒪 ?ㅼ틦??|
| `us_universe.py` | 誘멸뎅二쇱떇 ?좊땲踰꾩뒪 ?ㅼ틦??(?쒓?珥앹븸/?좊룞??二쇰큺異붿꽭/SPY MA ?꾪꽣) |

---

## signals
- Path: `src/trading_signal/`
- Classes: `KrSignalEngine`, `FxSignalEngine`, `CryptoSignalEngine`, `KrOrderbookFilter`
- Responsibility: 吏꾩엯/泥?궛 ?쒓렇???앹꽦
- Entry Point: `engine.py`
- Related Modules: selector, risk, execution
- Config: `settings.yaml > entry`, `settings.yaml > exit`, `settings.yaml > strategy_crypto_breakout` (breakout_lookback, max_breakout_chase_pct, max_candle_body_pct, max_upper_wick_ratio, retest_confirm_enabled, retest_confirm_bars)

### Forbidden
- 二쇰Ц 吏곸젒 ?꾩넚 湲덉?
- ?ъ???吏곸젒 ?섏젙 湲덉?
- 釉뚮줈而?API 吏곸젒 ?몄텧 湲덉?
- ?쒖꽭 ?ъ닔吏?湲덉? (collector 寃곌낵留??ъ슜)

### Files
| File | Role |
|------|------|
| `kr_signal_engine.py` | KR 二쇱떇 ?쒓렇???붿쭊 |
| `fx_signal_engine.py` | FX ?쒓렇???붿쭊 |
| `crypto_signal_engine.py` | ?뷀샇?뷀룓 異붿꽭 ?뚰뙆 ?쒓렇??(2?④퀎 吏꾩엯: Phase1 媛먯??뭁hase2 ?뺤씤, 吏꾩엯 ?덉쭏 ?꾪꽣 3醫? ?먯젅/?몃젅?쇰쭅/?쒓컙 泥?궛) |
| `us_swing_signal_engine.py` | 誘멸뎅二쇱떇 ?ㅼ쐷 ?쒓렇??(?뚮┝/?뚰뙆 吏꾩엯, 5?④퀎 泥?궛, 醫낅ぉ ?ㅼ퐫?대쭅) |
| `kr_orderbook_filter.py` | KR 二쇱떇 ?멸? ?꾪꽣: BuyOrderbookScore(吏꾩엯 ?뺥빀??, SellOrderbookScore(留ㅻ룄 ?꾪뿕 9議곌굔) ?곗텧 諛??덉닔 留ㅻ룄踰?媛먯? |

---

## risk
- Path: `src/risk/`
- Classes: `RiskManager`, `CryptoRiskManager`
- Responsibility: 由ъ뒪??愿由?(?쇱씪 ?먯떎, ?ъ????쒕룄, ?ъ뒪?꾩튂, 肄붿씤 ?곗냽?먯젅/?ъ쭊???쒗븳)
- Entry Point: `manager.py`
- Related Modules: execution, signals
- Config: `settings.yaml > risk`, `settings.yaml > risk_crypto`

### Forbidden
- 二쇰Ц 吏곸젒 ?꾩넚 湲덉? (?뱀씤/李⑤떒 ?먮떒留?
- ?쒖꽭 ?섏쭛 湲덉?
- ?꾨왂 ?먯닔 怨꾩궛 湲덉?
- ?ъ???吏곸젒 ?섏젙 湲덉?

### Files
| File | Role |
|------|------|
| `risk_manager.py` | 怨듯넻 由ъ뒪??留ㅻ땲? (ABC) |
| `crypto_risk.py` | ?뷀샇?뷀룓 ?꾩슜 由ъ뒪??(?곗냽 ?먯젅 3?? ?ъ쭊??1?? ?쇱씪 ?먯떎 -3%) |
| `us_swing_risk.py` | 誘멸뎅二쇱떇 ?ㅼ쐷 由ъ뒪??(珥??몄텧 80%, ?뱁꽣 吏묒쨷 ?쒗븳, ?곗냽 ?먯떎 以묐떒) |

---

## execution
- Path: `src/execution/`
- Classes: `ExecutionEngine`, `TradingOrchestrator`, `TradeRecord`, `TradeJournal`
- Responsibility: 二쇰Ц ?ㅽ뻾, ?ъ???愿由? ?ㅼ??ㅽ듃?덉씠?? 嫄곕옒 湲곕줉
- Entry Point: `orchestrator.py`
- Related Modules: adapters, risk, signals, storage
- Config: `settings.yaml > orchestrator`, `settings.yaml > risk`
- Runtime note: KR orderbook watchlist is updated in-place, and warmup windows are now kept per symbol (newly added symbols only) so repeated `orderbook_warmup` blocking is avoided.
- Runtime note: market-specific tracking tick dispatch is now registry-based (`orchestrator_core/market_registry.py` + `orchestrator_market/*/module.py`).

### Forbidden
- ?꾨왂 ?먮떒 湲덉? (signals 寃곌낵留??ъ슜)
- ?뱁꽣/醫낅ぉ ?먯닔 怨꾩궛 湲덉?
- 釉뚮줈而??묐떟 raw ?곗씠?곕? ?대? 紐⑤뜽 ?泥대줈 ?ъ슜 湲덉?

### Files
| File | Role |
|------|-----|
| `orchestrator.py` | ?몃젅?대뵫 硫붿씤 猷⑦봽. KR/FX/Crypto ?쒖옣蹂?tick. ?먯옄??吏꾩엯(DB?좏뻾?뭕roker?뭖onfirm/rollback), ?ъ???媛먯궗 |
| `state_machine.py` | RuntimeState (9?④퀎) ?곹깭 愿由?諛?transition 濡쒖쭅 (BomTS Runtime Uptime & Recovery v3.0) |
| `health_check.py` | HealthChecker ?쒖뒪???ㅽ듃?뚰겕 ?ъ뒪 泥댄겕, Mode (PAPER/LIVE) 蹂?諛섏쓳 寃곗젙 濡쒖쭅 |
| `wake_up.py` | WakeUpSequence ???쒖옉 ???섏〈??泥댄겕 二쇨린 ?섑뻾 |
| `orchestrator_core/contracts.py` | 留덉폆 紐⑤뱢 理쒖냼 怨꾩빟(`MarketModuleProtocol`) ?뺤쓽 |
| `orchestrator_core/market_registry.py` | `market -> module` 留ㅽ븨 ?덉??ㅽ듃由?|
| `orchestrator_market/runtime.py` | 留덉폆蹂?runtime dataclass 而⑦뀒?대꼫 (`KR/US/FX/CRYPTO`) |
| `orchestrator_market/kr_stock/module.py` | KR tracking tick dispatch 紐⑤뱢 |
| `orchestrator_market/us_stock/module.py` | US tracking tick dispatch 紐⑤뱢 |
| `orchestrator_market/us_stock/logic.py` | 湲곗〈 US tick/entry/exit 濡쒖쭅 ?닿? ?뚯씪 |
| `orchestrator_market/fx_fut/module.py` | FX tracking tick dispatch 紐⑤뱢 |
| `orchestrator_market/crypto/module.py` | Crypto tracking tick dispatch 紐⑤뱢 |
| `us_orchestrator.py` | ?명솚??shim (?ㅼ껜 濡쒖쭅? `orchestrator_market/us_stock/logic.py`) |
| `execution_engine.py` | 二쇰Ц ?쒖텧/?ъ???愿由?(`TRADING_ENV` + broker target mismatch hard gate ?ы븿) |
| `trade_journal.py` | TradeJournal v2: DB+Redis+JSON ?ㅼ쨷 ??? `open_trade()`??confirm_entry()`??close_trade()` / `rollback_trade()` |
| `pending_order_tracker.py` | PendingOrderTracker: SUBMITTED 二쇰Ц 異붿쟻. register?뭖onfirm_fill/cancel/timeout ?앸챸二쇨린. CORE-1~6 援ы쁽 |
| `position_auditor.py` | ??留덉폆 怨듭슜 ?ъ???媛먯궗/媛뺤젣 泥?궛. `close_all_positions()`, `audit_positions()` |

### 4-Dict Authoritative Runtime (orchestrator.py)

嫄곕옒 ?곗씠?곗쓽 ?좎씪???먮낯(SSOT). journal/DB/cache?????蹂듦뎄 ?꾩슜.

| Dict | Type | ?ㅻ챸 |
|------|------|------|
| `today_trading_by_market` | `dict[str, dict]` | 嫄곕옒 ?대깽??(entries, closed_trades, open_positions, orders, candidates) |
| `account_by_market` | `dict[str, dict]` | 怨꾩쥖 ?곹깭 (equity, balance, currency, updated_at) |
| `symbol_index_by_market` | `dict[str, dict]` | 醫낅ぉ 硫뷀? (name, theme, category) |
| `pipeline_by_market` | `dict[str, dict]` | ?뚯씠?꾨씪??(scan?뭚iltered?뭩cored?뭨anked?뭙ntry_candidates?뭙xcluded) |

| Method | ??븷 |
|--------|------|
| `_init_market_dicts()` | 4媛?dict 珥덇린 shape 援ъ꽦 |
| `get_today_trading(market)` | 嫄곕옒 ?곗씠??accessor |
| `get_account(market)` | 怨꾩쥖 accessor |
| `get_symbol_index(market)` | 醫낅ぉ 硫뷀? accessor |
| `get_pipeline(market)` | ?뚯씠?꾨씪??accessor |
| `_sync_closed_trade(market, row)` | 泥?궛 ??closed_trades + symbol_index ?숆린??|
| `_sync_account(market, info)` | ?붽퀬 ??account_by_market ?숆린??|
| `compute_session_stats(market)` | closed_trades 湲곕컲 P&L 吏곸젒 怨꾩궛 |
| `_last_scan_result` (property) | pipeline_by_market["KR_STOCK"]["_scan_result"] ?곌껐 |
| `_fx_sync_broker_state()` | FX ?몃? 泥?궛 媛먯? (journal OPEN - broker OPEN 李⑥쭛?? 2??miss rule) |
| `_session_record_buy(market, symbol, record)` | 吏꾩엯 湲곕줉 ??today_trading_by_market.entries |
| `_session_record_sell(market, symbol, record)` | 泥?궛 湲곕줉 ??today_trading_by_market.closed_trades (RULE UI-1: name 誘몄??? |
| `remove_market(market_str)` | 鍮꾪솢???붿씪 留덉폆 ?쒓굅 (07:30 由щ??????ㅼ?以꾨윭媛 ?몄텧) |

### Safety Guards (orchestrator.py)
| 媛??| ?ㅼ젙 ??| 湲곕낯媛?|
|------|---------|--------|
| 留ㅻ룄 ???ъ쭊???湲?| `risk.sell_cooldown_sec` | 180珥?|
| 醫낅ぉ???쇱씪 留ㅼ닔 ?쒗븳 | `risk.max_buy_per_symbol_daily` | 7??|
| ?꾩껜 ?쇱씪 留ㅼ닔 ?쒗븳 | `risk.max_buy_total_daily` | 20??|
| ?ъ???媛먯궗 二쇨린 | `risk.position_audit_interval_sec` | 3600珥?(1?쒓컙) |

### Atomic Trade Flow (trade_journal.py + orchestrator.py)
```
DB INSERT(PENDING) + Redis event  ?? broker submit  ??  ?깃났: DB UPDATE(OPEN) + Redis position = confirm_entry()
  ?ㅽ뙣: 5珥??ъ떆????DB DELETE + Redis DEL = rollback_trade()
       Redis 濡ㅻ갚 ?ㅽ뙣 ?? trade_undo_log + trade:undo stream
```

---

## replay
- Path: `src/replay/`
- Classes: `ReplayRunner`, `ReplayResult`
- Responsibility: ?뵺 諛깊뀒?ㅽ듃 ?쒕??덉씠??(**?낅┰ ?ㅽ뻾**: `run_test.py` 寃쎌쑀)
- Entry Point: `replay_runner.py`
- Related Modules: signals, execution
- Config: `settings.yaml > backtest`

---

## report
- Path: `src/report/`
- Classes: `ReportGenerator`, `PerformanceReport`, `Dashboard`, `MonitorAPI`
- Files: `reporter.py`, `dashboard.py`, `monitor_api.py`
- Responsibility: ?곗씪由?二쇨컙/?붽컙 由ы룷?? ????쒕낫?? 怨듦컻 紐⑤땲?곕쭅, AI 遺꾩꽍 由ы룷??- Entry Point: `reporter.py`, `dashboard.py`
- Related Modules: storage, execution
- Config: `settings.yaml > reporting`, `settings.yaml > orchestrator > monitor_port`, `settings.yaml > report_crypto`

### Forbidden
- adapters/ 吏곸젒 ?몄텧 湲덉? (INV-011)
- 鍮꾩쫰?덉뒪 ?곗씠??吏곸젒 怨꾩궛 湲덉? (execution 寃곌낵留??쎄린)
- 嫄곕옒 ?곹깭 ?섏젙 湲덉? (Read-Only)
- ?ъ????붽퀬 API 吏곸젒 ?ы빐??湲덉?

### Files
| File | Role |
|------|------|
| `reporter.py` | ?쇱씪/二쇨컙/?붽컙 由ы룷??+ 二쇨컙醫낇빀(4留덉폆) AI 遺꾩꽍 |
| `dashboard.py` | ????쒕낫??(FastAPI) |
| `monitor_api.py` | ?뵺 紐⑤땲?곕쭅 API (**?낅┰ FastAPI ?쒕쾭**) |
| `crypto_reporter.py` | ?뷀샇?뷀룓 ?쇱씪 蹂닿퀬??(JSON: ?밸쪧/?먯씡鍮?醫낅ぉ蹂?P&L ?? |
| `dashboard_watchdog.py` | ?뵺 ??쒕낫??媛먯떆 ?꾨줈?몄뒪 (**?낅┰ ?ㅽ뻾**: ??쒕낫??鍮꾩젙?????먮룞 ?ъ떆?? |

### Route Notes
- `routes/common_api.py`
  - `/api/status` ??`data_source`, `fallback_level`, `is_stale`, `degraded` 瑜??④퍡 諛섑솚?쒕떎.
  - `/health` ??orchestrator ?곌껐 ?щ?, runtime cache freshness, 理쒖떊 QA ?곹깭瑜??몄텧?쒕떎.
- `run.py --status`
  - 濡쒖뺄 ?곹깭 議고쉶??HTTP ?곗꽑?대ŉ, SSL ?몄쬆?쒓? ?쒖꽦?붾맂 ??쒕낫?쒖뿉?쒕뒗 HTTPS fallback???ъ슜?쒕떎.
- `routes/admin_api.py`
  - `/admin/api/chart/{symbol}` ???몃? 釉뚮줈而?API 吏곸젒 議고쉶 ???`chart_builder.collect_candle_data()` 湲곕컲 storage read model留??ъ슜?쒕떎.
  - `/admin/api/exchange-rate` ??`cache/exchange_rate.json` read model留??쎄퀬 ?몃? HTTP瑜??몄텧?섏? ?딅뒗??
- `routes/message_admin_api.py` [v4.1 NEW]
  - Message Admin API: `GET/PUT /admin/api/messages/templates`, `GET/PUT /admin/api/messages/policies`
  - `GET /admin/api/messages/channels`, `POST /admin/api/messages/channels/{id}/test`
  - `GET /admin/api/messages/log`, `POST /admin/api/messages/republish`
  - `GET /admin/api/messages/stats` (?듦퀎: 24h 諛쒖넚/?쒕∼/?ㅽ뙣 移댁슫??
- `routes/message_admin_page.py` [v4.1 NEW]
  - `/admin/messages` ?쇱슦??HTML ?뚮뜑留? 5????쒕낫??(媛쒖슂/Templates/Policies/Channels/Logs)
  - SSE 諛곕꼫: `web.banner.alert` ?대깽??30s ?대쭅 fallback?쇰줈 CRITICAL 諛곕꼫 ?쒖떆/?댁젣

### Public Pages (doc/html/)
| File | Route | Role |
|------|-------|------|
| `public_dashboard.html` | `/` | ?꾨━誘몄뾼 ?쒕뵫 ?섏씠吏 (?쒖뒪???뚭컻, ?꾪궎?띿쿂, ?섏씡 怨듦컻) |
| `public_monitor.html` | `/monitor` | ?쒖뒪??紐⑤땲?곕쭅 (?명봽???쒕퉬??嫄곕옒 ?쒕룞 ?꾪솴) |
| `public_admin_showcase.html` | `/showcase` | ?몃? PR???쇱??댁뒪 (UI 援ъ꽦/?쒖뒪???꾩꽦??媛뺤“) |
| `public_showcase.html` | `/docs/showcase` | 怨듦컻 臾몄꽌 寃쎈줈???쇱??댁뒪 ?섏씠吏 |

### Admin Pages (v4.1 ?좉퇋)
| Route | Module | Role |
|-------|--------|------|
| `/admin/messages` | `message_admin_page.py` | Message Admin UI 5????쒕낫??|

### Public API
| Endpoint | Role |
|----------|------|
| `/api/public/summary` | ?쒕쾭 ?곹깭, ?ㅻ뒛 ?뺤젙 P&L, 嫄곕옒 嫄댁닔 |
| `/api/public/monitor` | ?명봽??留덉폆 ?쒕퉬???곹깭 (?ы듃/IP ?쒓굅) |
| `/api/reports/weekly-latest` | 理쒓렐 二쇨컙 醫낇빀 由ы룷??4媛?諛섑솚 |
| `/admin/api/report-html/{type}/{date}` | HTML 由ы룷??吏곸젒 ?쒕튃 |

### Message Admin API (v4.1 ?좉퇋)
| Endpoint | Method | Role |
|----------|--------|------|
| `/admin/api/messages/stats` | GET | 24h 諛쒖넚 ?듦퀎 移대뱶 |
| `/admin/api/messages/templates` | GET/PUT | 硫붿떆吏 ?쒗뵆由?CRUD |
| `/admin/api/messages/policies` | GET/PUT | 諛쒖넚 ?뺤콉 CRUD |
| `/admin/api/messages/channels` | GET | 梨꾨꼸 ?덉??ㅽ듃由?議고쉶 |
| `/admin/api/messages/channels/{id}/test` | POST | 梨꾨꼸 ?뚯뒪??諛쒖넚 `[TEST]` |
| `/admin/api/messages/log` | GET | 諛쒖넚 ?대젰 (?꾪꽣: severity/status/market/time) |
| `/admin/api/messages/republish` | POST | ?대깽???щ컻??|

### Operation Scripts
| File | Role |
|------|------|
| `script/operation/weekly_scheduler.py` | ?쇱슂??08:00 二쇨컙 AI 醫낇빀 由ы룷???앹꽦 |
| `script/operation/run_fx_live.py` | FX ?좊Ъ ?쇱씠釉??몃젅?대뜑 |
| `script/operation/run_crypto_live.py` | ?뷀샇?뷀룓 ?쇱씠釉??몃젅?대뜑 |
| `script/operation/run_orchestrator.py` | ?ㅼ??ㅽ듃?덉씠??(KR/US) |

### DB Scripts (v4.1 ?좉퇋)
| File | Role |
|------|------|
| `script/db/schema_v11_message_admin.sql` | message_template/policy/channel/log 4媛??뚯씠釉??ㅽ궎留?|
| `script/db/seed_v11_message_admin.sql` | 28媛??쒗뵆由?+ 33媛??뺤콉 + 3媛?梨꾨꼸 珥덇린 ?쒕뱶 |

---

## storage
- Path: `src/storage/`
- Classes: `DBEngine`, `BarRepository`, `RedisClient`
- Responsibility: PostgreSQL ORM/?덊룷吏?좊━, Redis ?ㅼ떆媛??대깽???쒖뼱 ?ㅽ듃由? ?ㅽ궎留?- Entry Point: `db.py`, `redis_client.py`
- Related Modules: common, collectors, execution
- Config: `.env > PG_DSN`, `.env > REDIS_URL`
- Runtime note: storage SQL references are aligned with singular DB tables (`bar_1m`, `signal_event`, `trade_order`, `fill`, `sector_ranking`, `account_snapshot`, `risk_event`, `trade_record`, `theme`, `stock`, `premium_report`, `leader_stock`).
- Runtime note: `table_contract.py` resolves physical table names at runtime (singular first, plural fallback) so mixed-schema environments remain operable until DB migration is completed.
- Runtime note: physical DB table migration to singular contract was applied on 2026-04-11 (legacy plural table names removed in public schema).

### Forbidden
- 鍮꾩쫰?덉뒪 ?먮떒 湲덉? (???議고쉶留?
- ?꾨찓??紐⑤뜽 ?ъ젙??湲덉? (`common/models.py` ?ъ슜)
- ?꾩쓽 而щ읆/?뚯씠釉?異붽? 湲덉? (schema 踰꾩쟾 愿由??꾩닔)

### Files
| File | Role |
|------|----- |
| `table_contract.py` | logical table -> physical table resolution (singular first, plural fallback) with cache |
| `db.py` | SQLAlchemy 2.0 ?붿쭊/?몄뀡 ?깃???|
| `repositories.py` | bar_1m, signal_event, trade_order, fill ?덊룷吏?좊━ |
| `theme_repository.py` | theme, leader_stock, theme_stock_map CRUD |
| `stock_repository.py` | stock_master CRUD, 醫낅ぉ紐끸넂肄붾뱶 議고쉶(罹먯떆) |
| `orderbook_repository.py` | ?멸? ?ㅻ깄?????議고쉶 (?④굔쨌諛곗튂쨌?대젰) |
| `trade_journal_repository.py` | trade_journal/trade_undo_log DB CRUD (upsert/delete/undo) |
| `redis_client.py` | Redis ?깃???(fail-safe). Stream: `trade:events`, `system:log`, `trade:undo`, `notification:event`, `notification:confirm`, `notification:halt`. Hash: `trade:active:{symbol}` |

### Redis Keys
| Key Pattern | Type | ?⑸룄 |
|-------------|------|------|
| `trade:events` | Stream | 嫄곕옒 ?앹븷二쇨린 ?대깽??(open/entry/close/rollback) |
| `trade:active:{symbol}` | Hash | ?ㅼ떆媛??ъ???(trade_id, price, qty) |
| `system:log` | Stream | ?쒖뒪???대깽??(heartbeat, alert) |
| `system:heartbeat` | String | 理쒓렐 ?섑듃鍮꾪듃 (TTL 5遺? |
| `trade:undo` | Stream | Redis 濡ㅻ갚 ?ㅽ뙣 媛먯궗 濡쒓렇 |
| `notification:event` | Stream | 硫붿떆吏 ?붿쭊 ?낅젰 ?대깽??(durable IPC) |
| `notification:confirm` | Stream | ?댁쁺???뺤씤(confirmed) ?대깽??|
| `notification:halt` | Stream | ACK timeout 湲곕컲 ?먮룞 ?뺤? ?붿껌 |
| `notification:dedupe:*` | String(TTL) | 臾몃㎘ 湲곕컲 以묐났 ?쒓굅/?ㅻ줈? 寃뚯씠??|

### DB ?뚯씠釉??꾩껜 紐⑸줉
| Table | Schema File | ?⑸룄 |
|-------|------------|------|
| `symbol` | `schema.sql` | 醫낅ぉ 留덉뒪??|
| `tick` | `schema.sql` | ???곗씠??|
| `bar_1m` | `schema.sql` | 1遺꾨큺 |
| `sector_ranking` | `schema.sql` | ?뱁꽣 ??궧 |
| `signal_event` | `schema.sql` | ?쒓렇??媛먯궗 濡쒓렇 |
| `trade_order` | `schema.sql` | 二쇰Ц ?앸챸二쇨린 |
| `fill` | `schema.sql` | 泥닿껐 湲곕줉 |
| `account_snapshot` | `schema.sql` | 怨꾩쥖 ?ㅻ깄??|
| `risk_event` | `schema.sql` | 由ъ뒪???대깽??|
| `trade_record` | `schema_v2.sql` | 嫄곕옒 湲곕줉 ?뺤옣 ?뺣낫 |
| `theme` | `schema_v3_themes.sql` | ?뚮쭏 留덉뒪??|
| `stock` | `schema_v3_themes.sql` | 醫낅ぉ ?뺤옣 ?뺣낫 |
| `theme_stock_map` | `schema_v3_themes.sql` | ?뚮쭏-醫낅ぉ 留ㅽ븨 |
| `leader_stock` | `schema_v3_themes.sql` | ??μ＜ 湲곕줉 |
| `stock_master` | `schema_v4_stock_master.sql` | KIS 醫낅ぉ 留덉뒪??|
| `session_log` | `schema_v5_snapshots.sql` | ?몄뀡 濡쒓렇 |
| `premium_report` | `schema_v5_snapshots.sql` | ?꾨━誘몄뾼 由ы룷??|
| `sector_master` | `schema_v5_snapshots.sql` | ?낆쥌 留덉뒪??|
| `heartbeat` | `schema_v5_snapshots.sql` | ?쒕퉬???섑듃鍮꾪듃 |
| `code_display` | `schema_v6_code_display.sql` | 肄붾뱶 ?쒓? 留ㅽ븨 |
| `kr_orderbook_snapshot` | `schema_v7_orderbook_snapshot.sql` | KR ?멸? ?ㅻ깄??|
| `trade_journal` | `schema_v8_trade_journal.sql` | ?먯옄??嫄곕옒 湲곕줉 (PENDING?뭀PEN?묬LOSED) |
| `trade_undo_log` | `schema_v8_trade_journal.sql` | 濡ㅻ갚 ?ㅽ뙣 媛먯궗 濡쒓렇 |
| `trade_record` | (?섎룞 ?앹꽦) | 嫄곕옒 湲곕줉 (?덇굅?? 誘명솢?? |

---

## notifications
- Path: `src/notification/`
- Classes: `TelegramBot`, `BotRegistry`, `ResponseFormatter`, `Msg`, `CommandRouter`, `TelegramCommandHandler`, `SystemNotifier`, `TradeNotifier`, `TestNotifier`, `NotificationEvent`, `NotificationBridge`, `NotificationEngine`, `NotificationHistory`, `NotificationServiceManager`
- Responsibility: ?붾젅洹몃옩 硫?곕큸 + Redis Streams 湲곕컲 硫붿떆吏 ?붿쭊(?꾨줈?몄뒪 遺꾨━, ACK/Auto-Halt, policy/template/dispatch, SQLite WAL ?대젰)
- Entry Point: `bot_registry.BotRegistry.from_settings()`, `notification_service.start_notification_service()`
- Related Modules: execution, common
- Config: `settings.yaml > telegram`, `settings.yaml > notification.*`, `.env > TELEGRAM_*`

### Files
| File | Role |
|------|------|
| `telegram_bot.py` | HTTP ?대씪?댁뼵??(fire-and-forget, send_message) |
| `bot_registry.py` | 遊??깃????덉??ㅽ듃由?(6媛?遊?珥덇린?? |
| `formatter.py` | `ResponseFormatter` + `Msg` ?쒗뵆由?(?쒖? ?묐떟 ?뺤떇) |
| `command_router.py` | `CommandRouter` ??遊???낅퀎 ?덉슜 紐낅졊 ?뺤쓽 + halt/resume scope ?댁꽍 |
| `command_handler.py` | `TelegramCommandHandler` ???대쭅 + 沅뚰븳 寃利?|
| `system_notifier.py` | `SystemNotifier` ??startup/shutdown/heartbeat/alert/snapshot??durable event濡?諛쒗뻾 |
| `trade_notifier.py` | `TradeNotifier` ??signal/order/fill/exit/risk/flatten??durable event濡?諛쒗뻾 |
| `test_notifier.py` | `TestNotifier` ??test_start/success/fail |
| `notification_event.py` | `NotificationEvent` ??硫붿떆吏 ?붿쭊 怨듯넻 ?대깽???ㅽ궎留?(`occurred/enqueued/dispatched_at`, `ack_required`) |
| `notification_bridge.py` | producer helper ??notifier/run 寃쎈줈?먯꽌 Redis stream 諛쒗뻾 + direct fallback |
| `notification_engine.py` | consumer engine ??policy(dedupe/throttle/buffer), template(mask), dispatcher(retry/webhook), ACK timeout auto-halt |
| `notification_history.py` | SQLite WAL history store (`notification_record`) |
| `notification_service.py` | 硫붿떆吏 ?붿쭊 ?꾨줈?몄뒪 spawn/stop 留ㅻ땲? |

---

## app (Main Entry)
- Path: `src/app.py`
- Responsibility: ??븷 湲곕컲 ??吏꾩엯??(ROLE: all/core/execution/test)
- Entry Point: `main()`
- Related Modules: 紐⑤뱺 紐⑤뱢
- Config: `.env > NODE_ROLE` (`linux_main`/`mt5_node`) + `.env > ROLE`

---

## lib_test
- Path: `lib_test/`
- Responsibility: ?꾩껜 ?뚯뒪??肄붾뱶 (unit, integration, live)
- Entry Point: `pytest lib_test/`
- Config: `.env` (?뚯뒪???섍꼍 ?ㅼ젙)

---

## config/trade
- Path: `config/trade/`
- Files: `kr_stock.trade.yaml`, `fx_fut.trade.yaml`
- Responsibility: 留덉폆蹂?嫄곕옒 ?ㅼ젙 ?ㅻ쾭?쇱씠??- Related Modules: execution, risk

---

## scripts
- Path: `script/`
- Responsibility: DB ?ㅽ궎留? ?댁쁺/吏꾨떒 ?ㅽ겕由쏀듃, 臾몄꽌 ?앹꽦

### script/db/ ???곗씠?곕쿋?댁뒪 ?ㅽ궎留?
| ?뚯씪 | ?⑸룄 |
|------|------|
| `init_db.sql` | DB 珥덇린 ?앹꽦 (CREATE DATABASE, ROLE) |
| `schema.sql` | v1: 湲곕낯 ?뚯씠釉?(bar_1m, trade_order, fill ?? |
| `schema_v2.sql` | v2: session_log, trade_record, heartbeat ??|
| `schema_v3_themes.sql` | v3: theme, theme_stock_map, leader_stock ??|
| `schema_v4_stock_master.sql` | v4: stock_master, sector_master ??|
| `schema_v5_snapshots.sql` | v5: account_snapshot |
| `schema_v6_code_display.sql` | v6: code_display (肄붾뱶 ?쒖떆紐?愿由? |
| `schema_v7_orderbook_snapshot.sql` | v7: kr_orderbook_snapshot |
| `schema_v8_trade_journal.sql` | v8: trade_journal, trade_undo_log (?먯옄??嫄곕옒 湲곕줉) |

### script/operation/ ???댁쁺 & 吏꾨떒 ?ㅽ겕由쏀듃

#### ?? ?ㅽ뻾 (Runner)
| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `run_orchestrator.py` | ?꾩껜 ?몃젅?대뵫 ?ㅼ??ㅽ듃?덉씠???ㅽ뻾 | `src/execution/orchestrator.py` |
| `run_kr_leader.py` | KR ??μ＜ ?먯깋 + ?멸? ?섏쭛 猷⑦봽 | `src/selector/kr_scanner.py` |
| `run_crypto_live.py` | Crypto(Upbit) 釉뚮젅?댄겕?꾩썐 ?낅┰ 猷⑦봽 | `src/crypto/` |
| `run_fx_live.py` | FX(MT5) ?쇱씠釉?嫄곕옒 猷⑦봽 | `src/trading_signal/fx_signal_engine.py` |

#### ?뱤 由ы룷??& 臾몄꽌
| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `generate_reports.py` | ?쇱씪/二쇨컙 由ы룷???앹꽦 (??留덉폆) | `src/report/reporter.py` |
| `generate_daily_report.py` | ?뱀젙 ?좎쭨+留덉폆 ?쇱씪 由ы룷???섎룞 諛쒗뻾 | `src/report/reporter.py` |
| `generate_docs.py` | HTML 臾몄꽌 5醫??앹꽦湲? 湲곕낯? curated HTML 蹂댁〈(skip), `--force-overwrite`濡?紐낆떆??媛뺤젣 ??뼱?곌린 吏??| `doc/` |
| `weekly_scheduler.py` | 二쇨컙 醫낇빀 由ы룷???ㅼ?以꾨윭 (?쇱슂?? | `src/report/reporter.py` |

#### ?뵩 ?곗씠??愿由?| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `load_sectors.py` | KIS MST ?뚯씪濡?sector_master 媛깆떊 | `script/db/schema_v4` |
| `sync_code_display.py` | code_display ?뚯씠釉??숆린??(?щ낵 ?? | `script/db/schema_v6` |
| `recover_trades.py` | ?몄뀡 濡쒓렇?먯꽌 嫄곕옒 ?곗씠??蹂듦뎄 | `data/journal/` |
| `query_db.py` | 踰붿슜 DB 議고쉶 ?꾧뎄 (?ㅼ뼇??荑쇰━) | `src/storage/db.py` |
| `select_fx_symbols.py` | MT5 FX 嫄곕옒 ?щ낵 ?곸쐞 3媛??좎젙 | `src/selector/fx_symbol_ranker.py` ??李멸퀬: `data/symbol/fx_symbols.yaml` |
| `optimize_fx_params.py` | FX ?뚮씪誘명꽣 洹몃━???쒖튂 理쒖쟻??| `src/trading_signal/fx_signal_engine.py` |

#### ?㈉ 吏꾨떒 (Check)
| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `check_api.py` | scan-status API ?묐떟 ?뺤씤 (port 5007) | `src/web/dashboard.py` |
| `check_cache.py` | kr_status.json 罹먯떆 ?곗씠???뺤씤 | `cache/` |
| `check_db_status.py` | DB ?곌껐 諛??뚯씠釉??곹깭 ?뺤씤 | `src/storage/db.py` |
| `check_db_themes.py` | DB ?뚮쭏/?꾨━誘몄뾼 由ы룷???곗씠???뺤씤 | `src/storage/theme_repository.py` |
| `check_leader_pipeline.py` | ??μ＜ ?ㅼ틪 ?뚯씠?꾨씪??吏곸젒 ?ㅽ뻾 | `src/selector/kr_scanner.py` |
| `check_stock_master.py` | 醫낅ぉ 留덉뒪???뱁꽣 ?뺣낫 ?뺤씤 | `src/storage/repositories.py` |
| `check_name_match.py` | ?뚮쭏 留ㅼ묶 ?대쫫 鍮꾧탳 ?붾쾭洹?| `src/storage/theme_repository.py` |

#### ?㎦ ?뚯뒪??(Live)
| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `kr_trade_test.py` | KR 二쇱떇 ?쇱씠釉?留ㅻℓ ?뚯뒪??(KIS API) | `src/adapter/kr/kis_adapter.py` |
| `test_sector_api.py` | KIS Sector API URL ?뚯뒪??| `src/adapter/kr/kis_adapter.py` |
| `verify_fx_live.py` | MT5 ?꾨줉???곌껐 諛??섍꼍 寃利?| `src/adapter/fx/mt5_proxy.py` |

#### ?숋툘 ?쒖뒪??| ?뚯씪 | ?⑸룄 |
|------|------|
| `get_chat_id.py` | Telegram Bot Chat ID ?뺤씤 |
| `fx_session_mgr.py` | FX ?몄뀡 醫낅즺 ?쒓컙 愿由?|
| `kill_dashboard_ports.py` | ??쒕낫???ы듃 媛뺤젣 醫낅즺 |
| `restart_dashboard.py` | ??쒕낫???ъ떆??|
| `startup_preflight.py` | startup plan ?앹꽦 + 理쒖떊 QA/?쒕퉬??遺꾨━/留덉폆 寃곗젙 寃뚯씠??+ `TRADING_ENV`/broker target consistency gate |
| `startup_service.py` | WSL readiness ?뺤씤 ??preflight plan 湲곗??쇰줈 dashboard/trading ?쒕퉬??湲곕룞 |
| `heartbeat_watchdog.py` | 硫붿떆吏 ?붿쭊 鍮꾩쓽議??몃? watchdog. `/api/status` ?곗냽 ?ㅽ뙣 ??`/admin/api/kill-switch/activate` ?몄텧濡?out-of-band halt ?몃━嫄?|
| `wsl_start_ubuntu_background.vbs` | WSL Ubuntu 諛깃렇?쇱슫???쒖옉 |

#### ?뵇 QA (?쒖뒪???뺥빀??寃利?
| ?뚯씪 | ?⑸룄 | 愿??紐⑤뱢 |
|------|------|----------|
| `check_sot.py` | SoT 寃利?(.env/yaml/DB/Redis ?곌껐) | `src/common/config.py`, `src/storage/` |
| `tool/check_encoding.py` | ?띿뒪???뚯씪 ?몄퐫??BOM/EOL 寃利?+ Python ?띿뒪??I/O ?몄퐫??媛??| repo text files, `qa_runner.py` |
| `check_data_flow.py` | ?덉씠???섏〈???뺤쟻 遺꾩꽍 (grep+AST) | `doc/guideline/09_data_flow.md` |
| `check_runtime.py` | Trade ?곹깭 ?뺥빀??(DB/execution/Redis) | `src/storage/`, `src/execution/` |
|  | Runtime note: DB vs execution cutoff follows the current runtime day when a long-running session crosses midnight, so yesterday journal residue does not block today's QA. |  |
|  | Runtime note: same-day clean shutdown snapshot(`running=false`, empty execution state)? recent window 諛뽰씠?대룄 offline standard QA??execution-empty 洹쇨굅濡??ъ궗?⑸맂?? |  |
| `check_api.py` | Dashboard reachability + runtime source metadata + API/UI ?뺥빀??寃利?| `src/report/dashboard.py` |
| `audit_identifiers.py` | words.json 湲곗? ?앸퀎??媛먯궗 (?대옒???⑥닔/DB/config/env/module/json key) + changed-only/files/dir/tables/db-env 吏?? 寃곌낵瑜?`tmp/audit/audit_identifiers/*` ??꾩뒪?ы봽 ?뚯씪濡?異쒕젰. runtime ?ㅽ깘 諛⑹?瑜??꾪빐 `json_key` ?뺤떇寃?ъ? ?쇰컲 ?앸퀎??誘몃벑濡??⑥뼱??WARN 以묒떖?쇰줈 泥섎━?섍퀬, hard check??env/config ??諛?援ъ“ ?앸퀎?먯뿉 吏묒쨷. 異붽?濡?肄붾뱶 ?앸퀎?먯쓽 ?⑥닔/蹂듭닔 ?섎?濡?遺덉씪移섏? `[N]` ?⑦꽩 誘몃ℓ移??レ옄 ?앸퀎??寃쎄퀬瑜??먭? | `src/**`, `script/db/*.sql`, `config/settings.yaml`, `.env/.env.example`, DB schema introspection |
| `qa_runner.py` | QA ?듯빀 ?ㅽ뻾湲?(Quick/Standard/Full) + ?붾젅洹몃옩 ?꾩넚 + running.lock + qa_quick targeted identifier audit ?곗꽑?쒖쐞(`changed` -> `QA_IDENTIFIER_TARGETS` -> profile fallback, no-SKIP) + qa_full baseline gate(`config/qa/identifier_audit_baseline.json`) | `check_sot`, `check_data_flow`, `check_runtime`, `check_api`, `audit_identifiers.py` |
| `final_report_builder.py` | Task Manifest + QA artifact + git 蹂寃??뚯씪???쎌뼱 理쒖쥌 蹂닿퀬 珥덉븞 ?앹꽦 諛?`tmp/report/final/` artifact ???| `doc/plan/260413_last_report_plan.md`, `doc/reference/task_manifest/*`, `tmp/qa/*.json` |
| Admin QA API | `/admin/api/qa/latest`, `/history`, `/run`, `/api/qa/alert` | `admin_api.py` |
| Admin Final Report API | `/admin/api/final-report/preview`, `/admin/api/final-report/latest` | `admin_api.py`, `final_report_builder.py` |
| QA Dashboard | `/admin/qa` ??쒕낫??+ 寃쎄퀬 ?⑤꼸 | `pages.py` |

---

## collectors (?곗씠???섏쭛湲?
- Path: `src/collector/`
- Responsibility: ?몃? ?곗씠???뚯뒪 (Naver Premium, GoldenKey ?? ?섏쭛 諛?DB ???- Config: `config/settings.yaml > collectors`

### Files
| File | Role |
|------|------|
| `pre_market_report_scraper.py` | PMR(?μ쟾 由ы룷?? ?섏쭛湲? Provider: fire_ant_no1, Platform: naver_premium. Playwright+OCR+AI ?뚯씠?꾨씪??|
| `naver_premium_scraper.py` | DEPRECATED ??`pre_market_report_scraper.py` redirect shim (?섏쐞 ?명솚) |
| `goldenkey_collector.py` | GoldenKey ??μ＜ ?곗씠???섏쭛湲?|
| `stock_master_loader.py` | KRX 醫낅ぉ留덉뒪??濡쒕뜑 |
| `orderbook_collector.py` | KR ?멸? websocket ?섏쭛湲?(watchlist ?숆린??+ 1珥?latest snapshot 吏묎퀎 + fail-soft) |
| `orderbook_consumer.py` | ?멸? ?곗씠???뚮퉬/遺꾩꽍湲?|
| `mt5_collector.py` | MT5 FX/?좊Ъ ?곗씠???섏쭛湲?|
| `kr_orderbook_ws_client.py` | KIS KR ?멸? websocket client (subscribe/unsubscribe + reconnect backoff) |
| `kr_orderbook_watchlist.py` | KR ?멸? 媛먯떆 醫낅ぉ 愿由?(理쒕? 30, ?곗꽑?쒖쐞, FIFO ?쒓굅, 蹂댄샇 ?щ’) |
| `kr_orderbook_buffer.py` | 醫낅ぉ蹂?理쒓렐 1遺?second-snapshot 硫붾え由?踰꾪띁 |
| `kr_orderbook_aggregator.py` | 醫낅ぉ蹂???maxlen=5)?먯꽌 1珥?理쒖떊 ?대깽?몃쭔 異붿텧??snapshot ?앹꽦 |

### ?⑹뼱 泥닿퀎 (3-Tier)
| 怨꾩링 | ?앸퀎??| ?ㅻ챸 |
|------|--------|------|
| Tool (?뚮옯?? | `naver_premium` | 肄섑뀗痢??묎렐 ?섎떒 |
| Provider (?쒕퉬???쒓났?? | `fire_ant_no1` | 遺덇컻誘??띿씤湲?二쇱떇?섎쾭??|
| Content (肄섑뀗痢??좏삎) | `pre_market_report` (PMR) | ?μ쟾 由ы룷??|

---

## stock_classifier
- Path: `src/stock_classifier/`
- Classes: `GeminiClient`, `BatchManager`, `StockInfo`, `ClassificationRow`, `ParseResult`
- Responsibility: AI 湲곕컲 ?뚮쭏 以묒떖 醫낅ぉ 遺꾨쪟 + ?ㅼ떆媛?二쇰룄 ?뚮쭏 ?붿쭊
- Entry Point: `classifier/batch_manager.py:BatchManager.classify_weekly()`, `config.py:get_classifier_config()`
- Related Modules: `common/config`, `storage/db`, `execution/orchestrator`
- Config: `config/settings.yaml > stock_classifier`, `.env > GOOGLE_API_KEY_ahnda`

### Files
| File | Role |
|------|------|
| `config.py` | settings.yaml stock_classifier ?뱀뀡 ?꾩슜 濡쒕뜑 |
| `repository.py` | DB CRUD (stock_classification, theme_master, symbol_theme_map, trade_decision_log) |
| `classifier/gemini_client.py` | Gemini API ?섑띁 (rate limiting, ?ъ떆?? ?꾨＼?꾪듃 鍮뚮뜑) |
| `classifier/parser.py` | CSV ?뚯떛 + 寃利?(留덊겕?ㅼ슫 ?뺣━, 肄붾뱶 寃利? 以묐났 ?쒓굅) |
| `classifier/batch_manager.py` | 諛곗튂 遺꾪븷 + ?쒖감 ?몄텧 + 遺遺??ㅽ뙣 ?덉슜 |
| `classifier/weekly_classifier.py` | 二쇨컙 ?꾩껜 遺꾨쪟 (stock_master 濡쒕뵫, 12?쒓컙 荑⑤떎?? |
| `classifier/daily_patcher.py` | ?뱀씪 ?꾨낫 ?뚮쭏 ?ы솗??(?쒖옣 而⑦뀓?ㅽ듃 湲곕컲, PMR 李멸퀬) |
| `classifier/pmr_adapter.py` | PMR 由ы룷?????뚮쭏 ?곕룞 ?대뙌??(?덉갑 媛?? ?⑤룆 entry 遺덇?) |
| `service.py` | Canonical Resolver `resolve_theme()` + `resolve_sector()` |
| `prompts/system_prompt.txt` | Gemini ?쒖뒪???꾨＼?꾪듃 (怨듯넻) |
| `prompts/user_prompt_weekly.txt` | 二쇨컙 遺꾨쪟 ?꾨＼?꾪듃 (湲곗뾽 援ъ“ 湲곕컲) |
| `prompts/user_prompt_daily.txt` | ?쇰퀎 遺꾨쪟 ?꾨＼?꾪듃 (?쒖옣 而⑦뀓?ㅽ듃 湲곕컲) |
| `migrations/v001_create_tables.py` | 10媛??뚯씠釉?DDL (CHECK ?쒖빟 + ?뚰떚?붾떇) |
| `test/dry_run.py` | 10醫낅ぉ ?쒕씪?대윴 ?뚯뒪??|
| `test/test_phase2.py` | 17媛??⑥쐞?뚯뒪??(normalizer, scorer, lifecycle, manager) |
| `test/test_intraday.py` | 5媛??⑥쐞?뚯뒪??(scanner, leader state) |
| `theme/normalizer.py` | ?뚮쭏 ?대쫫 ?뺢퇋??+ alias 罹먯떆 + bigram ?좎궗??|
| `theme/scorer.py` | 6-Factor ?먯닔??(percentile rank, weight profile) |
| `theme/lifecycle.py` | 6?④퀎 ?곹깭 ?꾩씠 癒몄떊 |
| `theme/manager.py` | Theme Explosion 諛⑹? (auto-merge, pruning, cleanup) |
| `intraday/scanner.py` | IntradayScanner (?ㅼ떆媛??뚮쭏 ?ㅼ퐫?대쭅 + Leader Churn Guard) |
| `intraday/runtime.py` | ThemeRuntimeService (orchestrator ?곌껐 + DB ?곸냽?? |
| `cluster/correlation.py` | 1遺꾨큺 ?섏씡瑜??곴? 遺꾩꽍 (Pearson, 嫄곕━ 蹂?? |
| `cluster/engine.py` | DBSCAN ?대윭?ㅽ꽣留?(sklearn fallback, ?뚮쭏 ?먮룞 ?좊떦) |
| `leader/detector.py` | 4-factor ??μ＜ ?먯닔 + LeaderTracker (churn guard, 5-state) |
| `test/test_phase3.py` | 10媛??⑥쐞?뚯뒪??(correlation, clustering, leader) |
| `intraday/market_strength.py` | KOSPI 吏??湲곕컲 ?뚮쭏 ?먯닔 蹂댁젙 (0.5~1.2 factor) |
| `backtest/engine.py` | 諛깊뀒?ㅽ듃 ?붿쭊 (BacktestEngine + ReplayBacktestEngine: ?뚮쭏 ?ъ깮??+ decision log) |
| `backtest/replay_data.py` | DB 湲곕컲 怨쇨굅 ?곗씠??濡쒕뜑 (ReplayBacktestEngine ?낅젰?? |
| `test/test_e2e.py` | 16媛?E2E ?듯빀 ?뚯뒪??(market_strength, backtest, pipeline, 4 core scenarios) |

### DB Tables (10)
| Table | Purpose |
|-------|---------|
| `stock_classification` | AI 遺꾨쪟 寃곌낵 (?뺤쟻) |
| `stock_classification_history` | 遺꾨쪟 ?대젰 |
| `theme_master` | ?뚮쭏 留덉뒪??(6?④퀎 ?곹깭) |
| `theme_alias` | ?뚮쭏 蹂꾩묶 |
| `symbol_theme_map` | 醫낅ぉ?뷀뀒留?留ㅽ븨 (?ㅼ쨷 ?뚯뒪) |
| `intraday_theme_score` | ?μ쨷 ?뚮쭏 ?먯닔 |
| `intraday_theme_member` | ?μ쨷 ?뚮쭏 援ъ꽦??+ ??븷 |
| `cluster_snapshot` | ?대윭?ㅽ꽣留?寃곌낵 |
| `theme_score_daily` | ?뚮쭏 ?쇰퀎 吏묎퀎 |
| `trade_decision_log` | 留ㅻℓ ?섏궗寃곗젙 濡쒓렇 (?붾퀎 ?뚰떚?붾떇) |

## Session Snapshot Manager
- Path: src/execution/session_snapshot.py
- Classes: SessionSnapshotManager
- Responsibility: ?몄뀡 嫄곕옒 ?곗씠???곸냽??(dirty-flag + force_flush), ?먯옄????? ?ㅻ깄??蹂듦뎄, ?쇰퀎 諛깆뾽, 3媛쒖썡 珥덇낵 ?뺤텞
- Entry Point: SessionSnapshotManager(project_root)
- Related Modules: orchestrator (_snapshot_mgr), config (PROJECT_ROOT)
- Config: ?곸닔 ??FLUSH_INTERVAL_SEC=30, COMPRESS_AFTER_MONTHS=3
- Data Dir: data/runtime/today_trading_by_market.json, data/daily_trading/YYYY-MM/

## Entry Decision Logger
- Path: src/execution/entry_decision_log.py
- Classes: EntryDecision, GateResult, EntryDecisionLogger
- Responsibility: 留?吏꾩엯 ?됯? ?ъ씠?대쭏??寃뚯씠?몃퀎 pass/fail 湲곕줉, JSONL ?곸냽??(10??蹂닿?), 10遺??ㅻ깄?? 李⑤떒 ?듦퀎, ?붾젅洹몃옩 ?붿빟, **REJECT ?ъ쑀 援ъ“??湲곕줉**, EntryPath/DecisionResult enum re-export
- Entry Point: get_entry_decision_logger()
- Related Modules: orchestrator, kr_signal_engine, admin_api, symbol_state
- Config: config/settings.yaml > entry_decision (retention_days, snapshot_interval_min, max_candidates_per_cycle, shouting)
- API: /api/entry/debug, /api/entry/history, /api/entry/symbol-journey, /api/entry/snapshots, /api/entry/orderbook
- Data Dir: data/entry_decisions/{YYYY-MM-DD}/decisions.jsonl

## Symbol State Machine
- Path: src/execution/symbol_state.py
- Classes: SymbolStatus, EntryPath, DecisionResult (enums), SymbolState (dataclass), SymbolStateManager
- Responsibility: 醫낅ぉ蹂?吏꾩엯 ?곹깭癒몄떊 (IDLE?묬ANDIDATE?뭆HOUTING?묮NTERED?묮XITED), 吏?띿꽦 ?꾪꽣 (N???곗냽 ?뺤씤), shouting cooldown, ?μ큹諛?蹂댄샇 (market_open_guard)
- Entry Point: get_symbol_state_manager()
- Related Modules: orchestrator, entry_decision_log
- Config: config/settings.yaml > entry_decision.shouting (min_consecutive_ticks, cooldown_seconds, market_open_guard)

## Entry Monitor Dashboard
- Path: src/report/entry_monitor_page.py
- Classes: (none ??HTML template module)
- Responsibility: ??꾨씪??湲곕컲 吏꾩엯 ?먮떒 ?명룷洹몃옒????쒕낫?? ?ъ씠????꾨씪?? ?꾨낫 移대뱶, ?곸꽭 ?앹뾽, ?멸? ?앹뾽
- Guideline: [Entry Monitor Usage Guide](guideline/entry_monitor_usage.md)
- Entry Point: /admin/entry-monitor (pages.py ?쇱슦??
- Related Modules: entry_decision_log, admin_api (/api/entry/debug, /api/entry/orderbook)
- Config: config/settings.yaml > entry_mode, orderbook, entry_decision
- Data Source: /api/entry/debug (30珥??먮룞 媛깆떊)
- Notes: FX_FUT difficulty controls consume `/api/entry/debug` and `/api/entry/difficulty` using `profiles`, `active_profile`, and `current_profile` fields from admin_api.py.
- Notes: monitor shell text is kept charset-safe in `entry_monitor_page.py`, and `orderbook_relaxed_note` is normalized in `admin_api.py` to avoid duplicate or broken monitor copy.
- Notes: FX_FUT now preserves recent breakout memory across the pullback window and applies difficulty-driven Bollinger / mean-reversion thresholds from `src/common/fx_entry_mode.py` into `src/trading_signal/fx_signal_engine.py`.
## ReportGenerator (由ы룷???앹꽦湲?
- Path: src/report/reporter.py
- Classes: PerformanceReport, ReportGenerator
- Responsibility: ?쇱씪/二쇨컙/?붽컙 由ы룷??JSON+HTML ?앹꽦, AI ?됯? ?곕룞, 留덉폆蹂??붾젆?좊━ ???- Entry Point: ReportGenerator().daily_report() / weekly_report() / monthly_report()
- Related Modules: trade_journal, chart_builder, trade_notifier
- Config: config/settings.yaml > report (ai_model, schedule, chart, retry_count)
- Data Dir: data/reports/{MARKET}/{daily|weekly|monthly}/

## ChartBuilder (李⑦듃 ?곗씠??鍮뚮뜑)
- Path: src/report/chart_builder.py
- Classes: (none ??function module)
- Responsibility: 1遺꾨큺 DB 議고쉶 ??由ъ깦?뚮쭅 ??lightweight-charts JS 肄붾뱶 ?앹꽦, MA/留덉빱/援ш컙媛뺤“
- Entry Point: build_daily_chart_data(), generate_chart_html_section()
- Related Modules: reporter, repositories (get_bars)
- Config: config/settings.yaml > report.chart (cdn_url, timeframes, colors, moving_averages)

## Report Dashboard API
- Path: src/report/routes/common_api.py
- Classes: (FastAPI router)
- Responsibility: ??쒕낫??由ы룷??紐⑸줉/?곸꽭 API, ??寃쎈줈({MARKET}/{type}/) ?곗꽑 + ?덇굅??fallback
- Entry Point: /api/reports/{type}, /api/reports/{type}/{date}, /api/reports/weekly-latest
- Related Modules: reporter, dashboard
- Config: (none ??reads from data/reports/)

---

## KR 諛깊븘 ?뺤옣

### 異붽???紐⑤뱢
| Path | ??븷 |
|------|------|
| `src/storage/universe_repository.py` | KR 諛깊뀒?ㅽ듃 諛?諛깊븘???좊땲踰꾩뒪 ?곗씠?곕? ??ν븯怨?議고쉶?쒕떎. ?ㅽ궎留??곸슜, upsert, ?좎쭨蹂??좊땲踰꾩뒪 濡쒕뵫???대떦?쒕떎. |
| `src/storage/orderbook_repository.py` | KR ?멸? ?ㅻ깄????μ냼. legacy `kr_orderbook_snapshot` + second summary `kr_orderbook_second_snapshot` 諛곗튂 ??μ쓣 ?대떦?쒕떎. |
| `script/operation/backfill_kr_daily_top_value.py` | KIS ?쇰큺 ?곗씠?곕? 諛뷀깢?쇰줈 ?좎쭨蹂?嫄곕옒?湲??곸쐞 ?좊땲踰꾩뒪瑜??앹꽦?쒕떎. |
| `script/operation/backfill_kr_minute_bars.py` | ??λ맂 ?좊땲踰꾩뒪瑜?湲곗??쇰줈 KR 1遺꾨큺??`bar_1m`???곸옱?쒕떎. |

### ?섏젙??紐⑤뱢
| Path | 蹂寃??댁슜 |
|------|-----------|
| `src/adapter/kr/kis_adapter.py` | `inquire-daily-itemchartprice` ?몄텧??`get_daily_bars()`瑜?異붽??덈떎. |
| `src/storage/stock_repository.py` | KR ?꾩껜 ?쒖꽦 醫낅ぉ 濡쒕뵫??`list_active_kr_stocks()`瑜?異붽??덈떎. |

### 異붽????ㅽ궎留?| ?뚯씠釉?| ?ㅽ궎留??뚯씪 | ??븷 |
|--------|-------------|------|
| `daily_top_value_universe` | `script/db/schema_v9_kr_backfill.sql` | KR 醫낅ぉ???좎쭨蹂?嫄곕옒?湲??곸쐞 ?좊땲踰꾩뒪瑜???ν븳?? |
| `kr_orderbook_second_snapshot` | `script/db/schema_v10_kr_orderbook_second_snapshot.sql` | KR websocket ?멸?瑜?1珥?理쒖떊 snapshot + ?좏깮/蹂댁쑀/pending 而⑦뀓?ㅽ듃濡???ν븳?? |

---

## Guideline

| ?뚯씪 | ??븷 |
|------|------|
| `doc/guideline/06_glossary_rules.md` | ?⑹뼱 愿由?諛??⑥뼱 ?ъ쟾 洹쒖튃 (Glossary v0.4) |
| `doc/guideline/08_naming.md` | ?ㅼ씠諛?洹쒖튃 諛??쒖? |
| `doc/guideline/11_glossary_integration.md` | Glossary ?쒕툕紐⑤뱢 ? ?쒖뒪???곸슜 媛?대뱶 (AI 媛뺤젣, CI/CD, ?ъ쟾 怨듭쑀) |
| `.agents/workflows/new-identifier-procedure.md` | ?좉퇋 ?앸퀎???앹꽦 ?덉감 (?숈쓽??援먯감 寃???ы븿) |

## FxAnomalyWatchdog
- Path: src/execution/fx_anomaly_watchdog.py
- Classes: FxAnomalyWatchdog
- Responsibility: Watches for consecutive structural anomalies in FX order execution
- Entry Point: record_failure()
- Related Modules: src/execution/orchestrator.py
- Config: none
