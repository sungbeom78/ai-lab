# Session Log: AI Hub Instruction Review Pipeline MVP

- **작성 시각**: 2026-05-05 11:20 KST
- **작업 ID**: 260505_1058_ai-hub_ahnda_lostway_first_dev
- **담당**: Antigravity (AI Agent)

---

## 목표

ai-hub Local AI Console에 Instruction Review Pipeline MVP를 구현한다.
사용자 초안 지침을 3단계로 평가하여 opai 개발자에게 전달 가능한 Developer Request 문서를 생성한다.

---

## 구현 액션

### 새로 생성한 파일

| 파일 | 역할 |
|------|------|
| `app/local_ai_console/review_prompt_builder.py` | Stage 1/2/3 평가 프롬프트 생성 |
| `app/local_ai_console/instruction_review.py` | 3단계 평가 실행, 파일 저장, Google AI 연동 |
| `app/local_ai_console/developer_request_writer.py` | Developer Request 문서 생성 및 관리 |
| `config/google_eval_models.example.yaml` | Google AI 평가 설정 example (키 없음) |
| `out/developer-request/sample_drafts/ahnda_calendar_v1_draft.md` | ahnda 캘린더 개발 초안 |
| `out/developer-request/sample_drafts/ahnda_study_v1_draft.md` | ahnda 스터디 개발 초안 |
| `out/developer-request/sample_drafts/lostway_simulation_v1_draft.md` | lostway 시뮬레이션 초안 |

### 수정한 파일

| 파일 | 변경 내용 |
|------|-----------|
| `app/local_ai_console/main.py` | POST/GET /api/instruction-reviews, /api/developer-requests 추가 |
| `app/local_ai_console/templates/index.html` | 사이드바 탭 UI 전면 재구성 |
| `app/local_ai_console/static/style.css` | 다크 테마 사이드바 레이아웃 재작성 |
| `app/local_ai_console/static/app.js` | 탭 네비게이션, 평가 실행, 결과 표시 로직 추가 |

### 기타 생성 파일
- `/project/doc/service_idea_map.md`

---

## 추가된 API

| 메서드 | 경로 | 설명 |
|--------|------|------|
| POST | /api/instruction-reviews | 3단계 평가 실행 |
| GET | /api/instruction-reviews | 평가 목록 조회 |
| GET | /api/instruction-reviews/{review_id} | 특정 평가 조회 |
| GET | /api/developer-requests | Developer Request 목록 |
| GET | /api/developer-requests/{request_id} | 특정 Developer Request 조회 |

---

## 검증 결과

| 항목 | 결과 |
|------|------|
| Python 문법 검증 (`py_compile`) | ✅ OK |
| 서버 재시작 | ✅ 정상 기동 (port 11004) |
| `/api/health` | ✅ 200 OK |
| `POST /api/instruction-reviews` (local-only) | ✅ 200 OK |
| 파일 생성 확인 | ✅ v1~v4, metadata, summary, developer_request 모두 생성 |
| sample_drafts 3종 | ✅ 생성 완료 |

---

## 제한 사항

- `google-generativeai` pip 설치가 백그라운드에서 진행 중 (완료 후 Google AI 모드 사용 가능)
- local-only 모드에서는 실제 AI 평가 없이 구조 템플릿 반환
- Google AI 평가는 사용자 API key 입력 + `google-eval-required-later` 모드 선택 필요

---

## 다음 작업

1. google-generativeai 설치 확인 후 Google AI 모드 실제 테스트
2. ahnda 캘린더 sample_draft → Instruction Review → Developer Request 흐름 실전 검증
3. lostway simulation draft → 평가 → opai 전달 흐름 구성
4. `/project/site/ahnda` 개발은 ai-hub Developer Request 통해 진행
