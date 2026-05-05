# AI Hub Instruction Review Pipeline - BomTS 게시 준비

## 작업 요약

2026-05-05, ai-hub에 Instruction Review Pipeline MVP를 구현했다.

## 핵심 흐름

```
사용자 초안 지침
→ ai-hub 3단계 평가 (Stage 1/2/3)
→ Developer Request 문서 생성
→ opai 개발자에게 전달
→ 실제 개발 실행
→ 결과 기록
```

## 적용 대상 프로젝트

- **ahnda.com**: 캘린더, 스터디, 메모, 할 일, 작업 로그, 라이프 로그
- **lostway**: 위로형 상담 대화, synthetic conversation 생성
- **legacy-boardgame**: 시나리오 보드게임 엔진
- **bomTS-Decision**: 투자 결정 보조 (실거래 분리)

## 중요 정책

- **모든 개발 지시는 ai-hub를 경유**한다.
- Google AI 평가는 synthetic data에만, 사용자 승인 후 실행한다.
- Developer Request 문서에는 인간 승인 필요 항목이 명시된다.

## 기술 참고

→ `/project/ai-hub/doc/reference/bomts/20260505_112000_ai_hub_instruction_review_pipeline_reference.md`
