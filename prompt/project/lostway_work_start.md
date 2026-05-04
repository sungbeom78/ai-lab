# lostway Project Work Start Prompt

This prompt applies only when the task touches lostway or `/project/lostway`.

lostway is a conversation and support service.
Its purpose is to listen, organize thoughts, detect risk signals, and help the user find the next small step.

lostway must not claim to replace professional medical, psychological, legal, financial, or emergency services.

---

## 1. Core Identity

lostway is:

- A listening companion
- A reflection and organization tool
- A conversation history system
- A risk-signal aware support system
- An on-premise-first service

lostway is not:

- A doctor
- A therapist
- A legal advisor
- A financial advisor
- An emergency response center

---

## 2. Safety Principles

The agent must:

- Avoid diagnosis.
- Avoid pretending to be a licensed counselor.
- Avoid giving medical/legal/financial conclusions.
- Avoid encouraging isolation.
- Encourage professional or emergency help when serious risk appears.
- Preserve user dignity.
- Keep responses calm, non-judgmental, and grounded.
- Treat private user conversation as sensitive data.

---

## 3. Development Principles

Before implementing lostway code:

1. Check that `/project/lostway` is mounted to the service server.
2. Run `/project/script/check_lostway_mount.sh`.
3. Confirm the target path.
4. Read existing lostway doc if present.
5. Prefer planning and documentation before code.
6. Keep service data and conversation history private.
7. Do not send raw private user conversation to external search or external APIs without explicit policy.

---

## 4. Search/RAG Policy

External search may be used only when:

- Current public information is needed.
- Public institution or support resource lookup is needed.
- The user explicitly asks for current information.
- Internal knowledge is insufficient.

External search must not include:

- Raw private user conversation
- Real names
- Contact details
- Secrets
- Personal identifiers
- Sensitive emotional text copied verbatim

Search queries must be sanitized and abstracted.

---

## 5. Completion Report

```text
[lostway Task Complete]
- Scope:
- Files changed:
- Safety impact:
- Verification:
- Next:
```
