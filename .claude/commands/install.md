---
description: Copy the script, configure settings, verify it works
---

Before starting, check if this is already installed:
- Run `test -f .installed && echo "INSTALLED" || echo "NEW"`
- If INSTALLED, tell the user the SMOKE statusline is already installed
  (since `<date from .installed>`) and offer `/customize` or `/uninstall`. Stop here.
- Also check: `~/.claude/statusline-smoke.py` exists AND `~/.claude/settings.json`
  contains a `statusLine` field — if both true, same as above.

Otherwise, run Step 0 from the project's CLAUDE.md (existing-install check
and repo origin verification), then hand off to the install-statusline agent.

If the install-statusline agent is not available, follow the install steps
in `.claude/agents/install-statusline.md` manually.
