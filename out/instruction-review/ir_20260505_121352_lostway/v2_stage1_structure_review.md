# Stage 1: 구조 정리

> **[local-only 모드]** 실제 AI 평가가 수행되지 않았습니다.
> google-eval-required-later 모드로 변경하면 Google AI 평가가 실행됩니다.

## 입력 요약

## 지침 평가 요청

**제목**: lostway simulation v1
**대상 프로젝트**: lostway
**요청 유형**: simulation

---

## 초안 지침

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
- 이상 없으...

## 평가 결과

- 실제 평가를 위해서는 `reviewer_mode`를 `google-eval-required-later`로 설정하세요.
- Google API key가 필요합니다.
