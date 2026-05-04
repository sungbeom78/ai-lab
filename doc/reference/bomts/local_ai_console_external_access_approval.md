# 외부 네트워크 접속 승인 요청: Local AI Web Console

- 목적: 노트북 등 외부 기기에서 desktop-ai 내부의 Local AI Web Console 접속
- 목표 URL: `http://<DESKTOP_LAN_IP>:11004`
- 환경: Windows 11 호스트 내 WSL2 (Ubuntu 24.04)

## 사전 확인 값
- `<DESKTOP_LAN_IP>`: (PowerShell에서 `ipconfig`로 확인된 물리 IP)
- `<WSL_IP>`: `172.17.104.242`
- `<PORT>`: `11004`

## 승인 요청 작업

1. **Windows portproxy 등록 (필요 시)**
   WSL2 내부 포트(11004)를 Windows 호스트 포트(11004)로 포워딩합니다.
2. **Windows 방화벽 TCP 11004 Inbound 허용**
   노트북 등 다른 기기에서 호스트 PC의 11004 포트로 들어오는 연결을 허용합니다.

---

## 실행할 PowerShell 명령 (관리자 권한 필요)

```powershell
$ListenAddress = "<DESKTOP_LAN_IP>"
$ListenPort = 11004
$WslIp = "172.17.104.242"

# 기존 portproxy 삭제 (충돌 방지)
netsh interface portproxy delete v4tov4 listenaddress=$ListenAddress listenport=$ListenPort

# portproxy 추가
netsh interface portproxy add v4tov4 `
  listenaddress=$ListenAddress `
  listenport=$ListenPort `
  connectaddress=$WslIp `
  connectport=$ListenPort

# 방화벽 허용 (Inbound TCP 11004)
New-NetFirewallRule `
  -DisplayName "Local AI Console 11004" `
  -Direction Inbound `
  -Protocol TCP `
  -LocalPort 11004 `
  -Action Allow
```

## 확인 명령

```powershell
netsh interface portproxy show all
Get-NetFirewallRule -DisplayName "Local AI Console 11004"
```

## 되돌리기(Rollback) 명령

```powershell
$ListenAddress = "<DESKTOP_LAN_IP>"
$ListenPort = 11004

netsh interface portproxy delete v4tov4 `
  listenaddress=$ListenAddress `
  listenport=$ListenPort

Remove-NetFirewallRule -DisplayName "Local AI Console 11004"
```

## 보안 주의사항
- 11004 포트가 같은 내부 망(LAN)에 공개됩니다.
- 인증(Authentication) 기능이 포함되어 있지 않으므로, 신뢰할 수 없는 환경(공용 와이파이 등)에서는 보안상 위험할 수 있습니다.
- 작업 완료 후 반드시 승인 및 테스트를 진행해야 합니다.

- [ ] 사용자 승인 완료 (명령 실행 대기)
