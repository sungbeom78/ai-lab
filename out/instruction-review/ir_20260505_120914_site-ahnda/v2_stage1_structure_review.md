# Stage 1: 구조 정리

> **[local-only 모드]** 실제 AI 평가가 수행되지 않았습니다.
> google-eval-required-later 모드로 변경하면 Google AI 평가가 실행됩니다.

## 입력 요약

## 지침 평가 요청

**제목**: ahnda 캘린더 v1
**대상 프로젝트**: site-ahnda
**요청 유형**: development

---

## 초안 지침

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
   - `/project/site/ahnda/data/ca...

## 평가 결과

- 실제 평가를 위해서는 `reviewer_mode`를 `google-eval-required-later`로 설정하세요.
- Google API key가 필요합니다.
