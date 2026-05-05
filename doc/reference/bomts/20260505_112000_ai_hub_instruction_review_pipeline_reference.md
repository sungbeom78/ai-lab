# AI Hub Instruction Review Pipeline 기술 참고

## 개요

ai-hub Local AI Console에 3단계 지침 평가 파이프라인을 구현한 기술 기록이다.
ahnda.com, lostway, bomTS-Decision 등 모든 개발 지시가 이 파이프라인을 거친다.

---

## 서버 기동

```bash
bash /project/ai-hub/script/run_local_ai_console.sh
# PORT 기본값: 11004
```

---

## 핵심 모듈

| 파일 | 역할 |
|------|------|
| `review_prompt_builder.py` | Stage 1/2/3 system/user prompt 생성 |
| `instruction_review.py` | 3단계 평가 실행, 파일 저장 |
| `developer_request_writer.py` | Developer Request 문서 생성/조회 |

---

## API

### POST /api/instruction-reviews

```bash
curl -X POST http://localhost:11004/api/instruction-reviews \
  -H "Content-Type: application/json" \
  -d '{
    "title": "ahnda calendar v1",
    "target_project": "site-ahnda",
    "request_type": "development",
    "draft_instruction": "...",
    "reviewer_mode": "local-only",
    "temperature": 0.2
  }'
```

reviewer_mode 옵션:
- `local-only`: 실제 AI 호출 없음, 구조 템플릿 반환
- `google-eval-required-later`: Google AI API 호출 (google_api_key 필수)

### GET /api/instruction-reviews
### GET /api/instruction-reviews/{review_id}
### GET /api/developer-requests
### GET /api/developer-requests/{request_id}

---

## 파일 저장 구조

```
/project/ai-hub/out/instruction-review
  └─ ir_YYYYMMDD_HHMMSS_<project>/
      ├─ v1_original.md
      ├─ v2_stage1_structure_review.md
      ├─ v3_stage2_practical_review.md
      ├─ v4_stage3_final_approval.md
      ├─ review_metadata.json
      └─ review_summary.md

/project/ai-hub/out/developer-request
  ├─ <review_id>_opai_developer_request.md
  └─ <review_id>_opai_developer_request_metadata.json
```

---

## Google AI 모드 활성화

1. `google-generativeai` 설치 확인:
   ```bash
   /project/ai-hub/.venv/bin/pip install google-generativeai
   ```
2. UI에서 reviewer_mode를 `google-eval-required-later` 선택
3. Google API Key 입력 (세션에서만 사용, 저장 안 됨)

현재 설정된 모델:
- Stage 1: `gemini-2.5-flash-lite-preview-06-17`
- Stage 2: `gemini-2.5-flash-preview-05-20`
- Stage 3: `gemini-2.5-pro-preview-06-05`

---

## 보안 주의사항

- API key는 이 파일에 절대 기록하지 않는다.
- Google AI 평가는 synthetic data에만 실행한다.
- 실제 사용자 데이터는 Google AI에 전송하지 않는다.
- path traversal 방어: review_id, request_id에 `[a-zA-Z0-9_\-]` 외 문자 거부

---

## 검증 명령

```bash
# 문법 검증
python -m py_compile /project/ai-hub/app/local_ai_console/*.py

# 서버 상태
curl http://localhost:11004/api/health

# 평가 실행 (local-only)
curl -X POST http://localhost:11004/api/instruction-reviews \
  -H "Content-Type: application/json" \
  -d '{"title":"test","target_project":"site-ahnda","request_type":"development","draft_instruction":"테스트","reviewer_mode":"local-only","temperature":0.2}'

# 생성 파일 확인
find /project/ai-hub/out/instruction-review -maxdepth 3 -type f | sort
find /project/ai-hub/out/developer-request -maxdepth 3 -type f | sort
```
