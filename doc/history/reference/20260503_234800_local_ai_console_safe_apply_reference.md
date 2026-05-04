# Local AI Console Safe Apply Implementation

## Overview
This reference documents the implementation of the Phase 2 "Safe Apply" feature in the Local AI Console. This mechanism ensures that AI-generated files are applied safely to the file system using strict predefined rules and human-in-the-loop validation, mitigating risks such as path traversal and arbitrary code execution.

## Components
1. **API Router (`safe_apply.py`)**:
   - `GET /api/apply/site-ahnda-static-mvp/preview`: Dry-run mode that checks target files, backup statuses, and rule violations without writing to disk.
   - `POST /api/apply/site-ahnda-static-mvp`: Actual writer that validates rules, creates backups (`.bak_YYYYMMDD_HHMMSS`), and writes content.

2. **Security & Constraints**:
   - **Allowlist**: Only specific files (`index.html`, `assets/css/style.css`, etc.) can be modified.
   - **Path Traversal Protection**: Ensures absolute path of the target resolves within `AHNDA_BASE_DIR`.
   - **Sensitive Data Scanner**: Regex blocks keywords like `api_key`, `secret`, `password` and external URLs (`http://`, `https://`).

3. **Frontend (`app.js`, `index.html`)**:
   - Preview and Apply buttons added to the web UI.
   - Requires explicit `confirm()` before firing the `POST` request.

## Validation Strategy
- Validation requires user approval for production or service roots (`/project/site/ahnda`).
- Verify via `curl -s http://localhost:11004/api/apply/site-ahnda-static-mvp/preview`.
