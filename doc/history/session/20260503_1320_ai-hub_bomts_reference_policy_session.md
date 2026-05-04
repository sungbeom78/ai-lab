# Work Session: AI Hub BOMTS Reference Policy Update

## 1. Summary
- Date: 2026-05-03
- Project: ai-hub
- Task: Update and clarify bomts reference source vs publish-source policies
- Actor: Antigravity
- Mode: Auto-run
- Status: Completed

## 2. Goal
작업 이력 구조를 다시 점검하고, `reference/bomts` (기술 레퍼런스 원본)와 `publish-source/bomts` (게시 초안)의 역할을 명확히 분리하여 시스템에 각인시킵니다.

## 3. Context
1차 작업에서 이력을 ahnda용과 bomts용으로 분리했으나, 기술 레퍼런스의 원본을 저장할 위치(`reference/bomts`)가 확실히 규정되지 않았습니다. 실무 원본은 안전한 곳에, 가공된 글은 `publish-source`에 보관하여 혼선을 막고자 합니다.

## 4. Actions
| Step | Command / Action | Result | Note |
|---|---|---|---|
| 1 | `ls -la` | 성공 | 1차 작업 시 생성된 파일들의 정상 존재 여부 확인 |
| 2 | `mkdir -p` | 성공 | `/project/ai-hub/doc/reference/bomts` 디렉토리 확인/생성 |
| 3 | `replace_file_content` | 성공 | `ai_hub_work_start.md`에 bomts.net 로그 정책 명확화 업데이트 |
| 4 | 파일 내용 확인 | 성공 | `bomts_reference_template.md`에 요구된 필수 항목들이 모두 포함되어 있음 확인 |
| 5 | `write_to_file` | 성공 | 이전 작업(1차 작업)에 대한 `reference/bomts` 기술 원본 파일 생성 |
| 6 | 이력 문서 기록 | 성공 | 현 세션(`session`), `ahnda` 초안, `bomts` 초안 생성 |

## 5. Files Created / Updated
| File | Change |
|---|---|
| `/project/ai-hub/prompt/system/ai_hub_work_start.md` | bomts 기록 정책 수정 |
| `/project/ai-hub/doc/reference/bomts/20260503_1310_ai-hub_workspace_policy_reference.md` | 생성 (이전 작업 기술 원본) |
| `/project/ai-hub/doc/history/session/20260503_1320_ai-hub_bomts_reference_policy_session.md` | 생성 (현재 세션 기록) |
| `/project/ai-hub/doc/publish-source/ahnda/20260503_1320_bomts_reference_policy_log.md` | 생성 |
| `/project/ai-hub/doc/publish-source/bomts/20260503_1320_ai_hub_history_reference_policy.md` | 생성 |

## 6. Decision
| Decision | Reason |
|---|---|
| `reference`와 `publish-source`의 명확한 분리 | 기술 원본은 상세하지만 퍼블릭하기에 부담스러울 수 있음. 이를 분리하여 안전한 공개 체계를 확립 |

## 7. Error / Pending
| Item | Reason | Next |
|---|---|---|
| None | - | N/A |

## 8. Publish Source
### For ahnda.com
- `publish-source/ahnda/20260503_1320_bomts_reference_policy_log.md`

### For bomts.com / bomts.net
- `publish-source/bomts/20260503_1320_ai_hub_history_reference_policy.md`

## 9. Next Action
본격적인 `BomTS` 시스템 분석 혹은 이관 작업을 이 정책들 바탕 위에서 수행합니다.
