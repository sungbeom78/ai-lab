# Work Session: First Order Job History

## 1. Summary
- Date: 2026-05-03
- Project: ai-hub
- Task: Apply distinct history/publish policy for ahnda and bomts
- Actor: Antigravity
- Mode: Auto-run
- Status: Completed

## 2. Goal
AI Hub의 작업 이력을 단순한 일지가 아니라, "개인 회고용(ahnda.com)"과 "기술 재현용(bomts.net)"으로 명확히 분리하여 저장하는 정책을 적용합니다.

## 3. Context
모든 작업을 똑같은 템플릿으로 저장하면, 나중에 기술 블로그나 레퍼런스로 활용할 때 정보가 부족하거나 너무 장황해질 수 있습니다. 목적에 따라 기록의 형태를 분리하고 템플릿화하여 이후 작업들의 자산화 효율을 높입니다.

## 4. Actions
| Step | Command / Action | Result | Note |
|---|---|---|---|
| 1 | Directory listing | Success | `/project` 및 `prompt` 폴더 존재 확인 |
| 2 | `ai_hub_work_start.md` 수정 | Success | ahnda vs bomts 분리 정책 및 3대 기록 의무화 반영 |
| 3 | 템플릿 생성 | Success | `ahnda_publish_template.md`, `bomts_reference_template.md`, `session_log_template.md` 생성 |
| 4 | 이력 생성 | Success | 현재 세션 로그 및 publish-source(ahnda, bomts) 작성 |

## 5. Files Created / Updated
| File | Change |
|---|---|
| `ai_hub_work_start.md` | 수정 (Section 8 업데이트) |
| `ahnda_publish_template.md` | 생성 |
| `bomts_reference_template.md` | 생성 |
| `session_log_template.md` | 생성 |

## 6. Decision
| Decision | Reason |
|---|---|
| 이력 이원화 (ahnda / bomts) | 개인 로그와 기술 레퍼런스의 목적이 다르므로 템플릿과 저장 경로 분리 |
| 민감 정보 치환(`placeholder`) 의무화 | 기술 레퍼런스를 퍼블릭에 안전하게 공개하기 위한 최소한의 안전 장치 |

## 7. Error / Pending
| Item | Reason | Next |
|---|---|---|
| None | 파괴적/시스템 수정 작업이 포함되지 않음 | N/A |

## 8. Publish Source
### For ahnda.com
- `publish-source/ahnda/20260503_1310_ai-hub_workspace_policy.md` 생성됨.
### For bomts.com / bomts.net
- `publish-source/bomts/20260503_1310_ai-hub_workspace_policy.md` 생성됨.

## 9. Next Action
본 정책을 기반으로 향후 진행될 실제 환경 구축 및 코드 마이그레이션 작업을 수행하고 기록합니다.
