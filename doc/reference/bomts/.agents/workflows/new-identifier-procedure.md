---
description: Handling for unregistered glossary words via Telegram approval
---

# new-identifier-procedure

> Triggered when `audit_identifiers.py` reports an unregistered word in files
> touched by the current task, and the word is genuinely new after synonym and
> variant checks.

---

## 0. Absolute rules

When introducing a new identifier:
1. Auto-registration forbidden
2. Variant registration forbidden if base form already registered
   (`running` -> use `run`, `cancelling` -> use `cancel`, `states` -> use `state`)
3. Synonym registration forbidden if any synonym already registered
   (`transmit` -> use `send`, `abort` -> use `cancel`)
4. Genuine new word -> Telegram notification + user approval

---

## 1. Scanner-first check

Do not guess. Run the scanner.

```bash
python script/operation/audit_identifiers.py --changed-only
```

For targeted checks, use:

```bash
python script/operation/audit_identifiers.py --files src/path/file.py
python script/operation/audit_identifiers.py --dir src/execution
python script/operation/audit_identifiers.py --tables PG_DSN table_name
python script/operation/audit_identifiers.py --db-env PG_DSN
```

The scanner writes reports under:

```text
tmp/audit/audit_identifiers/
```

Inspect the generated report and handle only unregistered words relevant to
the current task.

### 1-A. Synonym cross-search (G-0)

For each unregistered word introduced by this task:

Define meaning -> list 3+ English synonyms -> look up each in
`glossary/dictionary/words.json` -> use any that are registered.

| Meaning | Candidates                    | Registered | Use    |
| ------- | ----------------------------- | ---------- | ------ |
| cancel  | cancel, abort, revoke         | cancel     | cancel |
| send    | send, transmit, dispatch      | send       | send   |
| start   | start, begin, launch          | start      | start  |
| create  | create, make, build, generate | create     | create |
| get     | get, fetch, retrieve          | get        | get    |

Only registration-candidate when none of 3+ synonyms are registered.

### 1-B. Variant check

If your candidate is a variant, check the base form:

| Variant attempt | Base form           | Action       |
| --------------- | ------------------- | ------------ |
| running         | run (registered)    | use `run`    |
| cancelling      | cancel (registered) | use `cancel` |
| states          | state (registered)  | use `state`  |
| sent            | send (registered)   | use `send`   |

Base form registered -> variant registration forbidden.

---

## 2. Branching after scanner + synonym/variant review

### Case A: Base form registered, variant attempted
**Stop, change code.** No Telegram needed. Use base form.

Example: `running_state` attempted -> rename to `run_state` or to a different
construct entirely.

### Case B: Synonym registered
**Stop, change code.** No Telegram needed. Use registered synonym.

Example: `transmit_signal` -> `send_signal`.

### Case C: Genuinely new word (Cases A and B both negative)
**Send Telegram, wait for user approval.**

#### Step C-1. Send notification

```bash
python script/operation/notify_new_identifier.py \
    --word "<word>" \
    --kind "root" \
    --meaning "<plain-text meaning>" \
    --source "<file:line>" \
    --synonyms-checked "<3 synonyms searched and result>" \
    --variant-check "<base form check>"
```

The script sends a plain-text message to the configured Telegram chat.

User receives:
```
BOM_TS Glossary - new word approval needed
----------------------------------
word: throttle
kind: root
meaning: API call rate limit
source: src/adapter/kr/kis_adapter.py:142
time: 2026-04-30 14:23:15 KST

synonym check: rate_limit, debounce, throttle all unregistered
variant check: throttle is base form (no variant)

approve: /glossary_approve throttle root
reject: /glossary_reject throttle
```

#### Step C-2. Halt the work

Pause the task. Do not proceed with the identifier until user response.

#### Step C-3. On approval

Register in `glossary/dictionary/words.json`:
```json
{
  "id": "throttle",
  "en": "throttle",
  "ko": "<Korean meaning>",
  "pos": "noun",
  "domain": "general",
  "description": "..."
}
```

Then:
```bash
python glossary/generate_glossary.py generate
```

Resume task.

#### Step C-4. On rejection

Pick a different word, restart from Section 1.

---

## 3. Why glossary is warn-only in pre-commit

`charter-glossary-warn` hook in `.pre-commit-config.yaml` runs the audit but
exits with code 0 (does not block commit). This is intentional:

- Existing code has hundreds of unregistered words (legacy)
- Blocking commits on legacy issues paralyzes work
- New identifiers are gated by **AI-side check** + Telegram approval, not by hook
- Legacy cleanup is a separate task

The control point is in this workflow, not in pre-commit.

---

## 4. Frequent failure patterns to avoid

| Attempted | Reason it fails | Correct action |
|-----------|-----------------|----------------|
| `transmit_data` | `send` registered | `send_data` |
| `running_status` | `run` registered | `run_status` |
| `abort_order` | `cancel` registered | `cancel_order` |
| `pos_calc` | `position` & `calculate` (`calc` is a registered abbreviation) registered | `position_calc` |
| `dispatch_event` | `send` registered (synonym) | `send_event` |

**The 9 unregistered words found in recent scan are likely from these patterns.**
Audit them first - probably 5-6 are variants/synonyms of registered words.

---

## 5. Setup requirements (one-time)

`.env` must contain:
```
TELEGRAM_BOT_TOKEN=<bot token>
TELEGRAM_CHAT_ID=<your chat id>
```

Test it:
```bash
python script/operation/notify_new_identifier.py \
    --word test --kind root --meaning test --source test:1 \
    --synonyms-checked "test" --dry-run
```

`--dry-run` prints message without sending.
