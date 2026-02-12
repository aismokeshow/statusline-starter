---
description: Copy the script, configure settings, verify it works
---

Before starting, check if this is already installed:
- Run `test -f .installed && echo "INSTALLED" || echo "NEW"`
- If INSTALLED, tell the user the SMOKE statusline is already installed
  (since `<date from .installed>`) and offer `/customize` or `/uninstall`. Stop here.
- Also check: `~/.claude/statusline-smoke.py` exists AND `~/.claude/settings.json`
  contains a `statusLine` field — if both true, same as above.

Otherwise, run Steps 0-0b from CLAUDE.md (existing-install check, origin
verification, and security scan), then hand off to the install-statusline
agent for Steps 1-7. Do not manually execute the install steps — the agent
handles everything.

If the install-statusline agent is not available, follow
`.claude/agents/install-statusline.md` from "Installation Steps" directly.
