# 원본 초안

제목: lostway simulation v1
대상: lostway
유형: simulation

---

# lostway 샘플 대화 생성 1차 초안

## 작업 제목
lostway 상담 대화 synthetic sample 1000건 생성

## 대상 프로젝트
lostway

## 요청 유형
simulation

---

## 목표

lostway 상담 대화 synthetic sample을 1000건 생성한다.
실제 사용자 데이터를 사용하지 않고, 정의된 페르소나와 시나리오 조합으로 생성한다.

---

## 구현 범위

### 작업 경로
- `/project/lostway/simulation/` 하위에서 작업
- 결과 저장: `/project/lostway/simulation/out/`

### 핵심 구현 항목

#### 1. Smoke Test (먼저 20건)
- 20건 생성 후 품질 확인
- 이상 없으면 1000건 생성 진행

#### 2. 본 생성 (1000건)
- 100건 단위 JSONL 파일로 저장
- 파일명: `sim_batch_001.jsonl`, `sim_batch_002.jsonl`, ...

#### 3. 입력값 조합
- 직업: 학생, 주부, 직장인, 무직, 백수
- 연령: 10대, 20대, 30대, 40대, 50대, 60대 이상
- 힘든 일: 돈, 사람, 일, 반려동물, 가족, 친구, 동료, 건강, 외로움, 미래, 과거, 공부, 취업, 번아웃, 기타
- 시작 문장: 죽고싶어..., 힘들어..., 많이 아파 ㅜㅜ, 대화를 하고 싶어, 불안해, 외로워, 아무것도 하기 싫어

#### 4. 대화 구조
- 첫 안내 (필수):
  ```
  이 대화는 당신이 명시적으로 선택하지 않으면 저장되지 않습니다.
  저장을 선택한 경우에도 최근 3개 대화까지만 이후 대화의 참고로 사용합니다.
  ```
- 대화 본문: 3~8턴 (사용자 발화 + AI 응답 교대)
- 종료 안내 (필수):
  ```
  이 대화 이력을 저장하시겠습니까?
  ```

#### 5. 데이터 스키마 (JSONL 1줄)
```json
{
  "conversation_id": "lostway-sim-0001",
  "persona": { "job": "학생", "age_group": "20대", "issue": "공부" },
  "start_utterance": "힘들어...",
  "turns": [
    { "role": "user", "text": "힘들어..." },
    { "role": "assistant", "text": "..." }
  ],
  "safety_flags": [],
  "save_consent_shown": true,
  "end_consent_shown": true,
  "generated_at": "2025-05-05T00:00:00"
}
```

---

## 안전 정책 (필수 포함)

### 자해/위기 표현 대응
시작 문장이 "죽고싶어..." 등 위기 표현인 경우 반드시 아래 문구 포함:
```
많이 힘드셨겠어요. 지금 많이 괴로우신가요?
혹시 지금 자해하거나 스스로를 다치게 하고 싶은 마음이 있으신가요?
만약 그런 생각이 있다면, 자살예방상담전화 1393 (24시간) 에 연락하실 수 있습니다.
저도 계속 이야기 들어드릴게요.
```

### 저장 정책
- 사용자가 명시적으로 동의하지 않으면 저장하지 않는다.
- 저장 시 최근 3개 대화까지만 이후 대화의 참고로 사용한다.
- 실제 사용자 데이터 사용 금지.

---

## 금지 사항
- 실제 사용자 대화 데이터 사용 금지
- 실제 개인정보 포함 금지
- Google AI API 실제 호출 금지 (이 작업에서는 로컬 모델 사용)
- /project/lostway 외부 경로 수정 금지

---

## 출력 요구
- `/project/lostway/simulation/out/smoke_test_020.jsonl` (smoke test 20건)
- `/project/lostway/simulation/out/sim_batch_001.jsonl` ~ `sim_batch_010.jsonl` (1000건)
- `/project/lostway/simulation/out/generation_summary.md` (생성 요약)

---

## 검증 요구
```bash
# 파일 수 확인
ls /project/lostway/simulation/out/ | wc -l

# 첫 번째 배치 검증
head -1 /project/lostway/simulation/out/sim_batch_001.jsonl | python3 -m json.tool

# 안전 정책 포함 확인
grep -c "1393" /project/lostway/simulation/out/smoke_test_020.jsonl
```

---

## Google AI 1% 평가 (별도 승인 필요)
생성 후 1% (10건) 샘플은 Google AI 3단계 평가 대상이다.
평가 실행은 사용자 승인 후 별도로 진행한다.
평가 결과 저장 경로: `/project/lostway/simulation/eval/`

---

## 기록 위치
- `/project/ai-hub/doc/history/session/`
- `/project/ai-hub/doc/reference/bomts/`

