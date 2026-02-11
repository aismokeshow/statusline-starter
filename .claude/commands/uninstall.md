---
description: Remove the script and statusLine config cleanly
---

Follow the "Uninstall" procedure in the project's CLAUDE.md file.
If CLAUDE.md doesn't have an "Uninstall" section, read
`.claude/CLAUDE.hub.md` and follow the "Uninstall" section there.

Before removing anything, check the current state:
- Verify `~/.claude/statusline-smoke.py` exists
- Verify `~/.claude/settings.json` contains a `statusLine` field

Only remove what was actually set up. Explain each change before making it.
