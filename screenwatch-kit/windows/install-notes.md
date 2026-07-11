# Windows install notes

1. Copy `capture-loop.ps1` to `%USERPROFILE%\screenwatch\bin\capture-loop.ps1`.
2. Register it to start at logon (run in a normal PowerShell/cmd, no admin needed):

```
schtasks /Create /TN Screenwatch /SC ONLOGON /TR "powershell -WindowStyle Hidden -ExecutionPolicy Bypass -File %USERPROFILE%\screenwatch\bin\capture-loop.ps1" /F
schtasks /Run /TN Screenwatch
```

3. Verify: within ~30 seconds, `%USERPROFILE%\screenwatch\days\<today>\` should contain `.jpg` frames and a `log.jsonl` whose lines have a non-empty `"app"`.

Control:
- Pause: `schtasks /End /TN Screenwatch`
- Resume: `schtasks /Run /TN Screenwatch`
- Remove: `schtasks /Delete /TN Screenwatch /F`

Notes:
- No permission prompts on Windows — screen capture just works for desktop apps.
- Black frames = DRM-protected content or an RDP session; that's expected.
- Multi-monitor: the script captures the primary display. An agent can extend it to all screens by iterating `[System.Windows.Forms.Screen]::AllScreens`.
- Browser URLs aren't captured (window titles include the page title, which covers most analysis). UI Automation-based URL capture is a possible upgrade if you want it.
- If `ffmpeg` is installed and on PATH, have your agent swap the JPEG save for WebP (`ffmpeg -i in.png -vf scale=1568:-2 -quality 35 out.webp`) for ~2× smaller files.
