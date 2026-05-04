# 기술 블로그 초안: AI 에이전트를 '조수'에서 '공동 개발자'로 승격시키는 위험도 기반 권한 설계

- Target:
  - [ ] ahnda.com
  - [x] bomts.com / bomts.net

## Draft Summary
초기 AI 셋업의 "무조건 금지(Forbidden by default)" 정책을 벗어나, 자율성을 보장하는 "위험도 기반 티어링(Risk-based Authority Tiers)"을 도입하여 실무 개발 속도를 극대화한 시스템 구조 개편 사례입니다.

## Background
보안과 시스템 안정성은 가장 중요하지만, 이를 지키기 위해 AI의 소스 코드 수정 권한 자체를 박탈해버리면 AI의 잠재력을 10%도 쓰지 못하게 됩니다. 매번 오타 수정이나 단순 스크립트 작성에까지 인간의 승인을 요구한다면 결국 병목(Bottleneck)이 발생합니다. 이에 따라 역할을 "읽기 전용 보조자"에서 "실질적 개발/운영 수행자"로 재정의할 필요가 생겼습니다.

## What was built or decided
**작업 모드와 권한 티어(Tiers)의 도입**
- **작업 모드의 세분화**: 전체 작업을 `Inspect, Prepare, Develop, Validate, Operate, Release` 6가지로 정의하여, AI가 스스로 자신이 현재 어떤 스탠스로 시스템에 접근하는지 자각하게 했습니다.
- **권한 체계 분리**: 
  - `Auto Allowed` & `Development Allowed`: 분석, 점검, 개발용 코드 수정 등은 묻지 않고 100% 자율화했습니다.
  - `Approval Required`: 실제 릴리즈, Git 푸시, 서버 포트포워딩 등 파급력이 있는 작업에 방지턱을 세웠습니다.
  - `Strong Approval Required`: 실거래 시스템(BomTS)의 API Key나 실제 서비스 사이트(`/project/site`) 등 치명적인 영역은 가장 엄격히 통제했습니다.

## Why it matters
"무조건적인 통제"보다 "정교한 선 긋기"가 보안과 생산성을 동시에 잡는 방법입니다. 특히 프로젝트별(`bomts`, `lostway`, `site`)로 리스크의 결이 다르기 때문에, 개발 허용 범위를 각각 다르게 설정하여 **유연하면서도 안전한 AI 작업 환경(AI Workspace)**을 완성했습니다.

## Technical details
- 시스템 지시문(`System Prompt`) 내 금지어("항상 금지")를 완화하고, 문맥적 제어 조건("특정 모드에서만 승인 필요")으로 변경.
- Development Allowed 구간의 코딩 작업에 대해 에디터(IDE)의 `Workspace Trust` 기능을 연동하여 완전 자동화 구현.

## Next step
이제 제한 없는(그러나 안전선은 그어진) 개발 모드 안에서, 실제 `bomts-ai` 내부 트레이딩 로직을 AI와 함께 분석하고 마이그레이션하는 고도화 작업에 돌입합니다.
