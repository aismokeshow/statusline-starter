# Vibe Coder's Guide to Your Statusline

You just installed a two-line status bar at the bottom of Claude Code. It tells you things Claude Code doesn't show by default — and the one thing it does show (context percentage), it shows more accurately than anything else.

Here's what you're looking at.

---

## Line 1: Where You Are

```
🔥 Opus │ ~/dev/my-project  main +2 ~1 (my-project)  #a1b2c3d4
```

Reading left to right:

| Part | What it means |
|---|---|
| 🔥 | Fire indicator — always lit, doubles (🔥🔥) when you hit the compact threshold |
| Opus | The model running this session |
| ~/dev/my-project | Your working directory (clickable — opens in Finder) |
| main | Git branch |
| +2 ~1 | 2 files staged, 1 modified |
| (my-project) | Clickable link to the GitHub repo |
| #a1b2c3d4 | Session ID — useful when you're running 5 instances |

Long paths get fish-abbreviated: `aismokeshow_build_in_public` becomes `ais…lic`. The clickable link always has the full path.

---

## Line 2: How Much Runway You Have

```
▰▰▰▰▰▰▱▱▱▱│▱▱▱▱▱▱▱▱▱▱ 32% 200k  ⏱ 4m 12s  $0.47  ↑24
```

| Part | What it means |
|---|---|
| ▰▰▰▰▰▰ | Filled portion of the progress bar — how much context you've used |
| │ | **The compact threshold marker** — where auto-compact fires |
| 32% | Context usage percentage |
| 200k | Total context window size |
| ⏱ 4m 12s | Session duration |
| $0.47 | Cost so far |
| ↑24 | Lines of code added this session |

---

## The Compact Threshold (The Whole Point)

Every other statusline shows the raw `used_percentage` from Claude Code. That number lies.

Claude Code reserves tokens for its response (~32K) and has a 13K internal safety buffer. So when your statusline says "80% used," Claude Code actually fires auto-compact at ~77%. You think you have room. You don't. Your session compacts and you lose momentum.

This statusline does the math. The `│` marker on the progress bar shows the *real* trigger point. When the filled portion reaches that marker, compact is about to fire.

**The color tells you how close you are:**
- **Orange** (ember) — normal, you have room
- **Yellow** (smolder) — approaching the threshold (85%+ of the way there)
- **Red** (coal) — at or past the threshold, compact is imminent

---

## The Fire

The 🔥 is always lit. That's the vibe — where there's smoke, there's code.

When context hits the compact threshold, it doubles: 🔥🔥. That's your heads-up to finish what you're doing before the session compacts.

---

## Customizing

Everything is changeable. Open Claude Code in the statusline-starter folder and say what you want:

```
/customize     change colors, bar style, thresholds, or hide elements
```

Some things people change:

- **Bar characters**: swap `▰▱` for `█░` or `●○` or `━─`
- **Colors**: the SMOKE palette is 6 ANSI colors — all swappable
- **Hidden elements**: don't care about cost? Hide it. Don't want git info? Hide it.
- **Bar width**: default is 20 characters, make it wider or narrower

---

## Where It Lives

Two files, that's the whole thing:

| File | Location |
|---|---|
| The script | `~/.claude/statusline-smoke.py` |
| The config | `~/.claude/settings.json` (the `statusLine` field) |

Changes to the script take effect on your next Claude Code interaction. No reload command needed.

---

## Quick Reference

| I want to... | Do this |
|---|---|
| Preview without installing | `python3 statusline-smoke.py --preview` |
| See the full demo | `python3 statusline-smoke.py --showcase` |
| Change colors or style | `/customize` in Claude Code |
| Reinstall if something broke | `/install` in Claude Code |
| Remove it completely | `/uninstall` in Claude Code |

---

## Something Broken?

The statusline just disappeared? Check two things:

1. **Script exists:** `ls ~/.claude/statusline-smoke.py`
2. **Config points to it:** check `~/.claude/settings.json` has a `statusLine` field

If both are there and it's still not showing, run `/install` to reset it.

Beyond that — it's a single Python script with zero dependencies. If Python 3.9+ runs on your machine, it works.
