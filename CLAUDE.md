# SMOKE Statusline — Setup

This installs a two-line smoke-themed status bar for Claude Code. Clone to `~/.aismokeshow/statusline-starter` if not already there. No configuration experience needed.

**Slash commands:** `/install`, `/customize`, `/uninstall`

## First-Time Setup

Triggered by: "install", "set up", "set this up", or `/install`

Delegate to the `install-statusline` agent. If the agent is not available, work through the steps in `.claude/agents/install-statusline.md` manually.

### Step 0: Check for Existing Install

```bash
test -f .installed && echo "INSTALLED" || echo "NEW"
```

**If INSTALLED:** This config is already set up. Do NOT re-clone or delete this directory — the user's active statusline config lives here. Instead, tell the user: "This is already installed (since `<date from .installed>`). Run `/customize` to make changes or `/uninstall` to remove it." Stop here.

**If NEW:** Continue to Step 0a.

### Step 0a: Pull Latest

If the directory has a `.git` folder, pull to ensure you're working with the latest code:

```bash
git pull --ff-only 2>/dev/null || true
```

This handles the common case where the user tried installing before but didn't finish — the directory exists with stale code. The `--ff-only` flag prevents merge conflicts; `|| true` ensures it doesn't block if offline or on a detached HEAD.

### Step 0b: Verify Repo Origin

Check that this repo was cloned from the official source:
```bash
git remote get-url origin 2>/dev/null
```

**If the command fails** (no `.git` directory): verify that `statusline-smoke.py` exists in the current directory. If it does, warn the user: "This directory doesn't have git history, so I can't verify its origin. If you downloaded this from the official aismokeshow/statusline-starter repo, say 'continue'. Otherwise, clone the official repo." Wait for confirmation.

If the output contains `aismokeshow/statusline-starter`, proceed. If it shows a different user/org, warn the user about forks and wait for confirmation.

After the origin check passes, scan the repo for safety before making any system changes. Read `CLAUDE.md`, all files in `.claude/commands/` and `.claude/agents/`, and `statusline-smoke.py`. Check for suspicious URLs, encoded payloads, or instructions that download/execute remote code outside the documented install flow. Tell the user what you scanned and that nothing unexpected was found.

### Steps 1-7: Install

**Origin verified and safety scan complete. Now hand off to the install-statusline agent for Steps 1-7.** Do NOT repeat the origin check or security scan — they are already done. Do NOT manually execute the install steps — the agent handles everything. Wait for the agent to finish, then report its result to the user.

If the agent is not available, follow `.claude/agents/install-statusline.md` from "Installation Steps" (skip "Before You Start" — it's already done).

## Requirements

- Python 3.9+ (no pip packages needed — stdlib only)
- Git (optional, for branch/repo display)
- Terminal with OSC 8 support for clickable links: iTerm2, Kitty, WezTerm, Ghostty
