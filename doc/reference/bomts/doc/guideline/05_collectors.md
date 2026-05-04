# 05. 수집기 규칙

> 상위: [README_AI_GUIDELINE.md](../README_AI_GUIDELINE.md)

---

## ★ 절대 규칙

> 새로운 웹사이트에서 데이터를 수집하는 작업을 추가할 때
> 아래 체크리스트를 반드시 완료해야 한다. 예외 없음.

---

## 체크리스트

- [ ] **1. 쿠키 도메인 등록**
  `config/settings.yaml` → `collectors.{collector_name}.cookie_domains` 에 도메인 추가.
  로그인 불필요 공개 사이트는 빈 리스트 `[]`.

- [ ] **2. 쿠키 매니저 등록**
  `src/common/cookie_manager.py` → `login_urls` dict에 해당 도메인의 `login_url`, `target_url` 매핑 추가.

- [ ] **3. 최초 쿠키 저장** (로그인 필요 사이트만)
  ```bash
  python -m src.common.cookie_manager <domain>
  ```
  브라우저에서 수동 로그인 → 쿠키 자동 저장 → `config/cookies/<domain>.json` 확인.

- [ ] **4. 쿠키 만료 감지 로직**
  로그인 페이지 리다이렉트 감지 시 자동 재로그인 프롬프트 표시.
  `cookie_manager.get_authenticated_page()` 사용 권장.

- [ ] **5. 문서 업데이트**
  - `doc/module_index.md` — 새 수집기 등록
  - `doc/change_log.md` — 변경 기록 추가
  - 이 파일 하단 등록 테이블 업데이트

---

## 현재 등록된 수집기

| 수집기 | 도메인 | 로그인 | 쿠키 파일 |
|--------|--------|--------|-----------|
| `naver_premium_scraper` | `naver.com` | ✅ 필요 | `config/cookies/naver_com.json` |
| `goldenkey_collector` | `goldenkey-top.vercel.app` | ✅ 필요 (Naver OAuth) | `config/cookies/goldenkey_full_auth.json` |

---

## KR 백필 수집기 메모

- `backfill_kr_daily_top_value.py`
  - 목적: KIS 일봉 데이터를 이용해 날짜별 거래대금 상위 유니버스를 생성한다.
  - 저장소: `daily_top_value_universe`
- `backfill_kr_minute_bars.py`
  - 목적: 저장된 유니버스를 기준으로 KR 1분봉을 백필한다.
  - 저장소: `bars_1m`

원칙:
- 전 종목 전체에 대해 3개월 1분봉을 한 번에 수집하지 않는다.
- 먼저 일봉으로 유니버스를 줄인 뒤, 그 유니버스만 1분봉을 수집한다.
- 새 수집기 스크립트를 추가하면 `doc/module_index.md`와 `doc/operations_manual.md`를 함께 갱신한다.
