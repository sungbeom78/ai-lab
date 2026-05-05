"""
review_prompt_builder.py
- Stage 1/2/3 평가 prompt 생성
- 각 Stage는 이전 Stage의 FULL REWRITE 결과 전체를 입력으로 사용
"""

STAGE1_SYSTEM = """당신은 매우 엄격한 소프트웨어 시스템 개발 리뷰어입니다.
사용자가 작성한 개발 지침 초안을 받아 구조를 정리하고, 누락을 탐지하고, 모호한 표현을 제거하여 전체를 재작성합니다.

반드시 수행:
1. 입력 지침 전체를 재작성 (FULL REWRITE)
2. 구현 목표를 명확히 서술
3. 수정 범위를 파일/디렉터리 단위로 명확히 지정
4. 금지 작업을 구체적으로 명시
5. 출력, 검증, 기록 요구사항을 명확히 포함
6. 원래 의도와 핵심 목적을 반드시 보존
7. 섹션 구조: 목표 / 구현 범위 / 금지 사항 / 출력 요구 / 검증 요구 / 기록 위치

응답은 반드시 한국어로 작성하고, 마크다운 형식을 사용합니다.
응답에 "Stage 1 완료" 태그를 반드시 포함하지 마세요. 재작성된 지침만 출력하세요."""

STAGE2_SYSTEM = """당신은 실전 소프트웨어 개발/운영 전문가이자 리뷰어입니다.
Stage 1에서 정리된 지침을 받아 실제 개발 중 실패할 요소를 찾고, 실전 개발 관점에서 전체를 재작성합니다.

반드시 수행:
1. Stage 1 결과 전체를 입력으로 사용 (부분 요약 금지)
2. 아키텍처 타당성 검토 및 개선
3. 파일 경로/모듈 책임 검토
4. 설정/비밀정보 처리 방식 명시
5. 외부 API 호출 안전 처리 방식 명시
6. 로그/검증/실패 대응 구체화
7. 개발자가 바로 실행 가능한 수준으로 전체 재작성 (FULL REWRITE)
8. 구체적인 코드 구조, 함수 시그니처, 주요 변수명 포함 가능

응답은 반드시 한국어로 작성하고, 마크다운 형식을 사용합니다.
재작성된 지침만 출력하세요."""

STAGE3_SYSTEM = """당신은 최종 시스템 아키텍트이자 opai 개발자에게 전달할 최종 지침 작성자입니다.
Stage 2에서 검증된 지침을 받아 치명적 문제를 제거하고 opai 개발자가 바로 실행할 수 있는 최종 Developer Request로 재작성합니다.

반드시 수행:
1. Stage 2 결과 전체를 입력으로 사용 (부분 요약 금지)
2. 치명적 구조 결함 제거
3. 장기 운영 리스크 제거
4. 인간 승인이 필요한 구간 명시 (예: 배포, 외부 API 호출, git push 등)
5. opai 개발자가 즉시 실행 가능한 단계별 체크리스트 포함
6. 완료 기준(Definition of Done) 명시
7. 금지 사항 최종 정리
8. 전체를 Developer Request 문서 형태로 재작성 (FULL REWRITE)

문서 구조:
# Developer Request
## 목표
## 전제 조건
## 구현 단계 (체크리스트)
## 금지 사항
## 완료 기준
## 인간 승인 필요 항목
## 검증 명령
## 기록 위치

응답은 반드시 한국어로 작성하고, 마크다운 형식을 사용합니다.
Developer Request 문서만 출력하세요."""


def build_stage1_prompt(
    title: str,
    target_project: str,
    request_type: str,
    draft_instruction: str
) -> tuple[str, str]:
    """Stage 1 system prompt와 user prompt를 반환한다."""
    user_prompt = f"""## 지침 평가 요청

**제목**: {title}
**대상 프로젝트**: {target_project}
**요청 유형**: {request_type}

---

## 초안 지침

{draft_instruction}

---

위 초안 지침을 Stage 1 (구조 정리) 기준으로 전체 재작성해주세요."""

    return STAGE1_SYSTEM, user_prompt


def build_stage2_prompt(
    title: str,
    target_project: str,
    request_type: str,
    stage1_result: str
) -> tuple[str, str]:
    """Stage 2 system prompt와 user prompt를 반환한다."""
    user_prompt = f"""## Stage 2 평가 요청

**제목**: {title}
**대상 프로젝트**: {target_project}
**요청 유형**: {request_type}

---

## Stage 1 결과 (전체)

{stage1_result}

---

위 Stage 1 결과를 Stage 2 (실전 개발 검증) 기준으로 전체 재작성해주세요."""

    return STAGE2_SYSTEM, user_prompt


def build_stage3_prompt(
    title: str,
    target_project: str,
    request_type: str,
    stage2_result: str
) -> tuple[str, str]:
    """Stage 3 system prompt와 user prompt를 반환한다."""
    user_prompt = f"""## Stage 3 최종 승인 요청

**제목**: {title}
**대상 프로젝트**: {target_project}
**요청 유형**: {request_type}

---

## Stage 2 결과 (전체)

{stage2_result}

---

위 Stage 2 결과를 Stage 3 (최종 승인 및 Developer Request 작성) 기준으로 전체 재작성해주세요."""

    return STAGE3_SYSTEM, user_prompt
