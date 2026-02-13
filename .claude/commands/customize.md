---
description: Change colors, bar width, thresholds, or hidden elements
---

Use the customize-statusline agent to handle this request.

Pass along whatever the user wants to change — colors, progress bar,
thresholds, element visibility, separators, or any other statusline
customization.

If the customize-statusline agent is not available, handle the request directly:

1. Read `~/.claude/statusline-smoke.py` (symlinked to the repo script) to understand
   the current state.
2. Read `.claude/CLAUDE.hub.md` for the customization quick reference
   (color map, segment line numbers, alternative character sets).
3. Read `docs/CUSTOMIZATION.md` for detailed reference with recipes.
4. Show the user what will change before applying.
5. After editing, verify with:
   ```bash
   echo '{"model":{"display_name":"Opus"},"workspace":{"current_dir":"/tmp/test"},"cost":{},"context_window":{"context_window_size":200000,"used_percentage":25},"session_id":"test1234"}' | python3 ~/.claude/statusline-smoke.py
   ```
