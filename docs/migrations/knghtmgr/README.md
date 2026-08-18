# knghtmgr client extraction

Source: `n-e-o-w-u-l-f/knghtmgr` at `044baeca25877a6e00bdda6df0553f05d4210dd3`.

The complete legacy CLI crate is preserved byte-for-byte under `legacy-source/crates/cli`.
Its behavior is distributed as follows:

- The local Rust `GameState` is not activated; `ApiClient` keeps the server authoritative.
- The rolling three-line display maps to the current reserved terminal renderer.
- The old shell-before-prompt idea is implemented by the `shellrpg-status` command.
- Optional `cacaview` execution is retained only as reference and is never invoked automatically.
- Prompt swapping maps to the current input and control-role workflow.

See `docs/shell-prompt-integration.md` for Bash, Zsh, and PowerShell setup.
The cross-repository 30-file disposition ledger is maintained in ShellRPG-server.

Verification:

```powershell
python -m pytest
python -m compileall -q src tests
git diff --no-index -- C:\Users\megal\Projekte\n-e-o-w-u-l-f\knghtmgr\crates\cli docs\migrations\knghtmgr\legacy-source\crates\cli
```
