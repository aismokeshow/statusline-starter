---
description: Copy the script, configure settings, verify it works
---

Before starting, check if the statusline is already installed:
- `~/.claude/statusline-smoke.py` exists
- `~/.claude/settings.json` contains a `statusLine` field

If both are true, tell the user the SMOKE statusline is already installed
and offer `/customize` to change it or `/uninstall` to remove it.

Otherwise, run Step 0 (Verify Repo Origin) from the project's CLAUDE.md,
then hand off to the install-statusline agent for Steps 1-7.

If the install-statusline agent is not available, follow the install steps
in `.claude/agents/install-statusline.md` manually.
