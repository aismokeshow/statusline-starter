# Customization

The fastest way to change anything is through Claude Code. Open a terminal in this folder, launch Claude Code, and type `/customize` followed by what you want. If you're not using Claude Code, expand the manual sections below each heading.

## Change the color palette

`/customize` — describe the theme or specific color you want (e.g., "switch to a Nord palette", "make the accent color cyan").

<details>
<summary><strong>Manual</strong></summary>

Find the `# ━━ SMOKE Palette` section in `~/.claude/statusline-smoke.py`. The palette uses ANSI 256-color codes in the format `\033[38;5;Nm` where N is a color number (0–255).

| Variable | Default | Code | Role |
|---|---|---|---|
| `WHITE` | bright white | `\033[97m` | Primary emphasis |
| `SILVER` | light gray | `\033[37m` | Secondary text, git staged |
| `ASH` | dark gray | `\033[90m` | Separators, muted info, git modified, lines removed |
| `EMBER` | orange 208 | `\033[38;5;208m` | Signature accent, session lines added |
| `COAL` | red 196 | `\033[38;5;196m` | Critical/danger |
| `SMOLDER` | yellow 220 | `\033[38;5;220m` | Warning zone |

Everything uses the 6-color SMOKE palette — no separate git colors. For a full theme swap, see the [theme presets](../themes/) or replace all 6 color variables manually. Reference: [ANSI 256-color chart](https://www.ditig.com/publications/256-colors-cheat-sheet).

</details>

## Change the progress bar

`/customize` — describe your preference (e.g., "make the bar 30 characters wide", "use block characters").

<details>
<summary><strong>Manual</strong></summary>

Search for these values in `~/.claude/statusline-smoke.py`:

- **Width:** `BAR_W` (search for `BAR_W = `, default `20`)
- **Fill character:** `▰` (in the bar-building `for` loop, search for `bar_chars.append`)
- **Empty character:** `▱` (same loop, the `else` branch)
- **Threshold marker:** `│` (same loop, the `compact_pos` branch)

Alternative character sets:

| Style | Fill | Empty |
|---|---|---|
| Default | `▰` | `▱` |
| Block | `█` | `░` |
| Dot | `●` | `○` |
| Dash | `━` | `─` |
| Pipe | `┃` | `│` |

</details>

## Tune warning thresholds

`/customize` — describe when you want colors to shift (e.g., "show warning at 60% instead of 70%").

<details>
<summary><strong>Manual</strong></summary>

**Fire indicator** (search for `# Fire indicator`): Controls when the fire emoji doubles.
- `pct >= compact_pct` or `exceeds_200k` → double fire `🔥🔥`
- Below that → single fire `🔥` (steady burn)

**Bar color zones** (search for `# Bar color shifts`): Colors shift relative to `compact_pct` (the auto-compact trigger point).
- `pct >= compact_pct` → `COAL` (red — you're past the danger line)
- `pct >= compact_pct * 85 // 100` → `SMOLDER` (yellow — approaching)
- Below that → `EMBER` (orange — normal)

The `compact_pct` value is computed from `CLAUDE_CODE_MAX_OUTPUT_TOKENS` and a 13K safety buffer. You can override it with the `CLAUDE_AUTOCOMPACT_PCT_OVERRIDE` environment variable.

</details>

## Hide or show elements

`/customize` — say what to hide or show (e.g., "hide the session ID", "remove cost display", "hide git info").

<details>
<summary><strong>Manual</strong></summary>

Each element is a segment variable in `~/.claude/statusline-smoke.py`. Set any segment to `""` to hide it. Search for the variable name to find it.

| Element | Variable | Search for |
|---|---|---|
| Fire indicator | `fire` | `fire = "🔥` |
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

</details>

## Common recipes

**Nord theme:**
```python
WHITE = "\033[38;5;231m"       # snow white
SILVER = "\033[38;5;146m"      # frost
ASH = "\033[38;5;60m"          # polar night
EMBER = "\033[38;5;110m"       # frost blue (accent)
COAL = "\033[38;5;131m"        # aurora red
SMOLDER = "\033[38;5;179m"     # aurora yellow
```

> More presets in the [`themes/`](../themes/) directory — Nord, Catppuccin Mocha, and Dracula ready to drop in.

**Minimal mode** — hide git, session, cost:
```python
git_seg = ""
session_seg = ""
cost_seg = f"{SILVER}{RST}"    # empty but preserves spacing
```

**Wide bar with block characters:**
```python
BAR_W = 40
# Then change ▰ to █ and ▱ to ░ in the bar-building loop
```

---

**Verification:** After any change, run this to confirm the script still works:

```bash
python3 ~/.claude/statusline-smoke.py --preview
```

Expected: two lines — a model/directory line with a fire emoji, and a progress bar line.
