# Shell prompt status integration

This is the server-authoritative successor to KnightMgr's three-line prompt status.
The installed `shellrpg-status` command performs a local-device login, reads
`GET /api/status/text`, prints exactly three lines, and fails silently when the
server is unavailable.

Defaults:

- Server: `http://127.0.0.1:8765`
- Character: `Ander`
- Timeout and authentication: handled by the ShellRPG API client
- State ownership: ShellRPG-server only

## Bash

Add to `~/.bashrc`:

```bash
shellrpg_status() {
  local out
  out="$(shellrpg-status 2>/dev/null)"
  if [ -n "$out" ]; then
    printf "%s\n" "$out"
  fi
}

if [[ -n "$PROMPT_COMMAND" ]]; then
  PROMPT_COMMAND="shellrpg_status; $PROMPT_COMMAND"
else
  PROMPT_COMMAND="shellrpg_status"
fi
```
## Zsh

Add to `~/.zshrc`:

```zsh
shellrpg_status() {
  local out
  out="$(shellrpg-status 2>/dev/null)"
  if [[ -n "$out" ]]; then
    print -r -- "$out"
  fi
}

precmd_functions+=(shellrpg_status)
```

## PowerShell

Add to `$PROFILE`:

```powershell
function global:ShellRpgStatus {
  try {
    $out = shellrpg-status
    if ($out) { Write-Host $out }
  } catch { }
}

$oldPrompt = $function:prompt
function global:prompt {
  ShellRpgStatus
  & $oldPrompt
}
```
## Options

Use a different endpoint, character, or account:

```text
shellrpg-status --base-url http://127.0.0.1:8765 --character-name Roman
shellrpg-status --account-id local-account
```

The command does not modify `PS1` or the existing PowerShell prompt body. It emits
no diagnostics by default, so an unavailable server does not pollute the shell.
