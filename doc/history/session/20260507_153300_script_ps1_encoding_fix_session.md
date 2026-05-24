# Session Log: PowerShell Script Encoding Fix

- **Date**: 2026-05-07 15:33:00 (KST)
- **Target**: `script/refresh_wsl_ssh_portproxy.ps1`
- **Goal**: Fix broken Korean text execution in Windows PowerShell while preserving the workspace policy of UTF-8 without BOM.

## Action Taken
1. Identified the root cause of mojibake: Windows PowerShell 5.1 attempts to read `.ps1` files without BOM using the system default codepage (CP949 in Korean Windows). Because the file is encoded in UTF-8 without BOM, the Korean multi-byte characters are incorrectly parsed.
2. The user has a strict policy of keeping all files encoded as UTF-8 without BOM to ensure broad compatibility with Linux (`pwsh` supports it natively).
3. Instead of introducing a BOM (which resolves Windows parsing but contradicts strict UTF-8 No BOM workspace policies), all Korean messages in `/project/script/refresh_wsl_ssh_portproxy.ps1` were translated to English.
4. Since ASCII characters are single-byte and identical across CP949 and UTF-8, this entirely avoids parsing errors in Windows `powershell.exe`.

## Files Changed
- Modified: `/project/script/refresh_wsl_ssh_portproxy.ps1`

## Validation
- Changed Korean output strings to English. File encoding remains UTF-8 without BOM.
- Verified file changes to ensure cross-platform compatibility without text corruption on Windows PowerShell execution.
