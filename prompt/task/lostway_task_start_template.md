# lostway Task Start Template

## 0. Task Identity

- Project: lostway
- Task name:
- Task type:
  - [ ] planning
  - [ ] document update
  - [ ] dialogue design
  - [ ] safety policy
  - [ ] data structure
  - [ ] backend code
  - [ ] frontend code
  - [ ] RAG/search
  - [ ] test
- Target path:
- Expected output:

---

## 1. Mandatory Check

Before working:

```bash
/project/script/check_lostway_mount.sh
```

If the mount check fails, stop.

---

## 2. Safety Check

```text
[Safety Check]
- Does this task involve user conversation data?
- Does this task involve mental health or crisis response?
- Does this task involve external API/search?
- Does this task send private data outside local environment?
- Does this task need explicit approval?
```

If private data may leave the local environment, stop and request approval.

---

## 3. Work Rules

* Prefer planning before code.
* Keep private conversation data local by default.
* Do not claim professional authority.
* Do not diagnose.
* Do not replace emergency services.
* Use calm and non-judgmental language.
* For crisis-related content, prioritize connection to real help.

---

## 4. Completion Report

```text
[lostway Task Complete]
- Scope:
- Files changed:
- Safety impact:
- Verification:
- Next:
```
