# 원본 초안

제목: ahnda 캘린더 v1
대상: site-ahnda
유형: development

---

# ahnda 캘린더 1차 개발 초안

## 작업 제목
ahnda.com 캘린더 탭 1차 개발

## 대상 프로젝트
site-ahnda

## 요청 유형
development

---

## 목표

/project/site/ahnda에 캘린더 탭을 구현한다.
1차는 정적 JSON 기반 월간 달력 grid를 중심으로 구현한다.

---

## 구현 범위

### 수정 가능한 경로
- `/project/site/ahnda` 하위 전체

### 핵심 구현 항목
1. 캘린더 탭 UI 추가
   - 월간 달력 grid (7열 × 6행)
   - 이전/다음 월 이동 버튼
   - 오늘 날짜 강조 표시
   - 날짜 클릭 시 해당 일정 목록 표시

2. 데이터 파일
   - `/project/site/ahnda/data/calendar.json` 생성
   - 샘플 일정 10건 포함
   - 스키마:
     ```json
     {
       "events": [
         {
           "id": "evt_001",
           "date": "2025-05-10",
           "title": "스터디 모임",
           "category": "study",
           "description": "알고리즘 스터디 3주차",
           "all_day": true
         }
       ]
     }
     ```

3. 카테고리
   - study (공부)
   - work (업무)
   - personal (개인)
   - health (건강)
   - etc (기타)

---

## 금지 사항
- Google Calendar API 실제 호출 금지
- Telegram Bot API 실제 호출 금지
- API key 생성/수정/출력 금지
- /project/site/ahnda 외부 경로 수정 금지
- DB 연동 금지 (1차는 정적 JSON만 사용)

---

## 향후 목표 (README에만 기록)
- Google Calendar 양방향 연동
- Telegram으로 일정 추가
- task registry 기반 자동 일정 등록
- change_log.md 작업 기록 기반 캘린더 등록
- 주간/일간 조회 추가

---

## 출력 요구
- 브라우저에서 캘린더 탭이 동작해야 한다
- 월간 달력이 정상 렌더링되어야 한다
- 샘플 일정이 달력에 표시되어야 한다
- 날짜 클릭 시 해당 일정이 표시되어야 한다

---

## 검증 요구
- 브라우저에서 /project/site/ahnda 진입 후 캘린더 탭 클릭
- 월 이동 버튼 클릭 시 이전/다음 달 이동 확인
- 오늘 날짜 강조 확인
- 샘플 이벤트 표시 확인

---

## 기록 위치
- `/project/ai-hub/doc/history/session/`
- `/project/ai-hub/doc/publish-source/ahnda/`

