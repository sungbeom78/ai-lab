# Remote Access Guide (노트북 Antigravity 접속 준비)

## 1. SSH Server (SSHD) 상태
- 데스크탑 WSL의 `ssh.service`가 활성화되어 현재 실행 중입니다.
- **현재 설정 (`/etc/ssh/sshd_config`)**:
  - `Port 7771` (계획의 2222 포트가 아닌 7771 포트를 사용 중입니다.)
  - `PubkeyAuthentication yes` (권장 상태)
  - `PermitRootLogin no` (권장 상태)
  - `PasswordAuthentication yes` (*권장 사항 아님, 보안을 위해 `no`로 변경 고려 필요*)

## 2. 노트북 `~/.ssh/config` 접속 예시
노트북에서 WSL 내부로 접속하기 위한 설정 예시입니다. (포트는 현재 설정된 7771을 기준으로 작성됨)

```text
Host desktop-wsl
    HostName <Windows_데스크탑_IP>
    User bomiyang
    Port 7771
    IdentityFile ~/.ssh/id_ed25519
```

## 3. Windows Portproxy 설정 스크립트 초안 (PowerShell)
데스크탑의 외부 IP로 들어오는 SSH 포트를 WSL 내부로 포워딩하는 명령입니다.

```powershell
# 관리자 권한으로 실행
$WSL_IP = (wsl hostname -I).Trim()
netsh interface portproxy add v4tov4 listenport=7771 listenaddress=0.0.0.0 connectport=7771 connectaddress=$WSL_IP
```

## 4. Windows 방화벽 규칙 생성 명령 초안 (PowerShell)
WSL SSH 포트(7771)에 대한 외부 접근을 허용합니다. (전체 개방이 아닌 특정 포트만 허용)

```powershell
# 관리자 권한으로 실행
New-NetFirewallRule -DisplayName "WSL SSH 7771" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 7771
```
