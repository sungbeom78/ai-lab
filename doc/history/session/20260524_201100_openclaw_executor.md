# AI Hub Work Session Log - 2026-05-24 (Conflict Guard Update)

- **세션 ID**: `20260524_201100_openclaw_executor`
- **목표**: 다중 모드 옵션을 여러 개 켰을 때(inspect, prepare, develop 등), 상호 충돌되는 제약조건("계획만 세워라" vs "코드를 완성해라") 때문에 모델이 인지적 교착 상태(Cognitive Conflict)에 빠져 요약만 출력하는 현상을 근본적으로 해결한다.
- **수행 유형**: Develop, Prompt Optimization

## 1. 구현 및 튜닝 사항 (Priority Override Rules)

### 1-1. 지침 우선순위 교통정리 핫픽스 (`instruction.py` 수정)
- **현상**: 스크린샷과 같이 모든 모드(`inspect, prepare, develop...`)를 켜둔 상태로 Qwen에게 요청 시, `inspect/prepare`의 "분석/계획만 하라"는 지침과 `develop`의 "코드를 직접 고치라"는 지침이 프롬프트 내에 공존하여 충돌하면서, 모델이 결국 코딩을 포기하고 수동 분석 리포트(1~5단계 단계 나열)만 출력하며 멈춤.
- **조치**: `/project/ai-hub/app/openclaw/instruction.py` 내의 `build_system_prompt` 함수에서 다중 모드 조립 로직을 전면 튜닝함.
- **합병 규칙(Critical Merge Rule)**: 다중 모드 목록 내에 **`develop` (개발) 모드가 단 하나라도 포함되어 있다면**, `inspect`나 `prepare` 모드의 보수적인 제약 조건은 자동으로 무력화(Override)하고 **"실제 소스코드(Proposed Files)의 완성을 무조건 1순위로 진행하라"**는 강력한 지시어를 동적으로 주입하여 모델의 인지 교착 상태를 완벽히 해결함.

---

## 2. 향후 계획 (Next Steps)
- 모든 옵션을 켜두고 지시해도, Qwen2.5-coder가 헷갈리지 않고 요약과 계획서를 다 걷어치운 채 `Proposed Files`에 실제 코드를 정밀하고 완벽하게 출력해내어, 파일에 실시간 물리적으로 쓰이는지 최종 테스트할 것.
