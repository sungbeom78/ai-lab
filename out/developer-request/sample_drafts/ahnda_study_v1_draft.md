# ahnda 스터디 1차 개발 초안

## 작업 제목
ahnda.com 스터디 탭 1차 개발 (Notion 이전 MVP)

## 대상 프로젝트
site-ahnda

## 요청 유형
development

---

## 목표

Notion에서 관리하던 스터디 페이지를 ahnda.com으로 이전할 수 있는 정적 MVP를 만든다.
1차는 study.json 기반 목록/카드/태그/진행 상태/링크 placeholder를 만든다.

---

## 구현 범위

### 수정 가능한 경로
- `/project/site/ahnda` 하위 전체

### 핵심 구현 항목
1. 스터디 탭 UI
   - 스터디 카드 목록 (grid 형태)
   - 태그 필터 (전체 / 알고리즘 / 언어 / 프레임워크 / AI / 기타)
   - 진행 상태 필터 (전체 / 진행 중 / 완료 / 보류)
   - 카드 클릭 시 상세 팝업 또는 expand

2. 데이터 파일
   - `/project/site/ahnda/data/study.json` 생성
   - 샘플 스터디 항목 8건 포함
   - 스키마:
     ```json
     {
       "studies": [
         {
           "id": "study_001",
           "title": "파이썬 알고리즘 기초",
           "tags": ["python", "algorithm"],
           "status": "in_progress",
           "start_date": "2025-03-01",
           "end_date": null,
           "description": "코딩테스트 준비를 위한 알고리즘 스터디",
           "progress": 60,
           "link": null,
           "notes": "백준 실버 목표"
         }
       ]
     }
     ```

3. 진행률 표시
   - progress bar (0~100%)
   - 상태 배지 (진행 중 / 완료 / 보류)

---

## 금지 사항
- Notion API 실제 호출 금지
- 실제 개인 스터디 데이터 사용 금지 (샘플 데이터만 사용)
- 이미지/첨부 파일 처리 없음 (향후 검토)
- /project/site/ahnda 외부 경로 수정 금지
- DB 연동 금지 (1차는 정적 JSON만 사용)

---

## 향후 목표 (README에만 기록)
- Notion API 연동으로 자동 동기화
- 이미지/첨부 파일: /project/site/ahnda/media 정책 검토
- 스터디 노트 Markdown 렌더링

---

## 출력 요구
- 스터디 탭에서 카드 목록이 정상 표시되어야 한다
- 태그 필터 동작 확인
- 진행 상태 필터 동작 확인
- 진행률 표시 확인

---

## 검증 요구
- 브라우저에서 /project/site/ahnda 진입 후 스터디 탭 클릭
- 태그 필터 클릭 시 필터링 동작 확인
- 진행 상태 필터 동작 확인

---

## 기록 위치
- `/project/ai-hub/doc/history/session/`
- `/project/ai-hub/doc/publish-source/ahnda/`
