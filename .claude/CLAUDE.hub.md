# SMOKE Statusline

This folder is your statusline command center. Open Claude Code here and ask for what you want — change colors, swap the progress bar style, adjust thresholds, or customize any visual element. You never need to edit the script manually.

**Slash commands:** `/install`, `/customize`, `/uninstall`

The instructions below tell Claude Code how to manage everything. You can read along if you're curious, but you don't have to.

## Project Architecture

```
statusline-starter/
├── CLAUDE.md                              ← Install-phase instructions (you're reading the hub replacement)
├── statusline-smoke.py                    ← The statusline script
├── docs/CUSTOMIZATION.md                  ← Human-readable customization guide with recipes
├── .claude/
│   ├── CLAUDE.hub.md                      ← THIS FILE — operational reference
│   ├── agents/
│   │   ├── install-statusline.md          ← Install agent (copy script, configure settings, verify)
│   │   └── customize-statusline.md        ← Customization agent (colors, bar, thresholds, segments)
│   └── commands/                          ← Slash command dispatchers (/install, /customize, /uninstall)
```

**Agents:**
- `install-statusline` — copies the script to `~/.claude/`, sets the `statusLine` field in settings.json, verifies, and switches to this hub CLAUDE.md
- `customize-statusline` — reads the live script, identifies what to change, confirms with the user, applies edits, and verifies

## How This Works

- `~/.claude/statusline-smoke.py` is the live script
- `~/.claude/settings.json` points Claude Code at it via the `statusLine` field
- Changes to the script take effect on the next Claude Code interaction (no reload needed)
- The script reads JSON from stdin and outputs two ANSI-formatted lines

## Customization Quick Reference

### Colors (the `# SMOKE Palette` section)

| Variable | Default | ANSI Code | Role |
|---|---|---|---|
| `WHITE` | bright white | `\033[97m` | Primary emphasis |
| `SILVER` | light gray | `\033[37m` | Secondary text, git staged |
| `ASH` | dark gray | `\033[90m` | Separators, muted info, git modified, lines removed |
| `EMBER` | orange 208 | `\033[38;5;208m` | Signature accent, session lines added |
| `COAL` | red 196 | `\033[38;5;196m` | Critical/danger |
| `SMOLDER` | yellow 220 | `\033[38;5;220m` | Warning zone |

ANSI 256-color format: `\033[38;5;Nm` where N is 0–255.

### Progress Bar

- **Width:** `BAR_W` variable (default `20`)
- **Fill character:** `▰` in the bar-building loop
- **Empty character:** `▱` in the bar-building loop
- **Threshold marker:** `│` in the bar-building loop — shows where auto-compact fires

Alternative character sets:

| Style | Fill | Empty |
|---|---|---|
| Default | `▰` | `▱` |
| Block | `█` | `░` |
| Dot | `●` | `○` |
| Dash | `━` | `─` |

### Thresholds

**Fire indicator** (the `# Fire indicator` block in BUILD LINE 1):
- `pct >= compact_pct` or `exceeds_200k` → double fire `🔥🔥`
- Below → single fire `🔥` (steady burn)

Two states only — fire is always lit, doubles at the compact threshold.

**Bar color zones** (the `# Bar color shifts with heat` block in BUILD LINE 2, relative to `compact_pct`):
- `>= compact_pct` → `COAL` (red — past the danger line)
- `>= compact_pct * 85 // 100` → `SMOLDER` (yellow — approaching)
- Below → `EMBER` (orange — normal)

### Environment Variables

| Variable | Effect |
|---|---|
| `CLAUDE_CODE_MAX_OUTPUT_TOKENS` | Output token reservation (default 32000). Affects compact threshold position. |
| `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` | Direct override for the compact trigger percentage. |

### Toggleable Elements

Each segment variable can be set to `""` to hide it. Use Grep to find these variables by name in the script.

| Element | Variable | Search for |
|---|---|---|
| Fire indicator | `fire` | `fire =` in the BUILD LINE 1 section |
| Model name | `model_seg` | `model_seg =` |
| Agent name | `agent_seg` | `agent_seg =` |
| Vim mode | `vim_seg` | `vim_seg =` |
| Directory path | `dir_seg` | `dir_seg =` |
| Drift indicator | `drift_seg` | `drift_seg =` |
| Git branch + stats | `git_seg` | `git_seg =` |
| Session ID | `session_seg` | `session_seg =` |
| 200k warning | `warn_seg` | `warn_seg =` |
| Duration | `dur_seg` | `dur_seg =` |
| Cost | `cost_seg` | `cost_seg =` |
| Lines changed | `lines_seg` | `lines_seg =` |
| Transcript link | `transcript_seg` | `transcript_seg =` |

## First-Time Setup

Triggered by: `/install`

If `.installed` exists in this directory, or `~/.claude/statusline-smoke.py` already exists and `~/.claude/settings.json` contains a `statusLine` field, tell the user everything is configured and offer `/customize` to change it or `/uninstall` to remove it.

Otherwise, the `install-statusline` agent handles the full setup. It copies the script, configures settings.json, and verifies the installation.

## Uninstall

Check the current state before removing anything. Only undo what was actually set up.

1. **Remove the statusLine field from settings.json:**
   Read `~/.claude/settings.json`, remove the `statusLine` key, and write it back. Preserve all other fields.

2. **Delete the script:**
   ```bash
   rm ~/.claude/statusline-smoke.py
   ```

Tell the user: "SMOKE statusline removed. The status bar will revert to Claude Code's default on your next interaction."

## Requirements

- Python 3.9+ (no pip packages needed — stdlib only)
- Git (optional, for branch/repo display)
- Terminal with OSC 8 support for clickable links: iTerm2, Kitty, WezTerm, Ghostty
