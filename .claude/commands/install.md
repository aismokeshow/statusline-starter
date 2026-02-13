---
description: Symlink the script, configure settings, verify it works
---

Before starting, check if this is already installed:
- Run `test -f .installed && echo "INSTALLED" || echo "NEW"`
- If INSTALLED, run `git pull --ff-only 2>/dev/null || true` to get latest,
  then verify `~/.claude/statusline-smoke.py` is a symlink to this repo
  (fix with `ln -sfn "$(pwd)/statusline-smoke.py" ~/.claude/statusline-smoke.py`
  if it's a stale copy). Tell the user it's up to date and offer `/customize`
  or `/uninstall`. Stop here.

Otherwise, run Steps 0-0b from CLAUDE.md (existing-install check, origin
verification, and security scan), then hand off to the install-statusline
agent for Steps 1-7. Do not manually execute the install steps — the agent
handles everything.

If the install-statusline agent is not available, follow
`.claude/agents/install-statusline.md` from "Installation Steps" directly.
