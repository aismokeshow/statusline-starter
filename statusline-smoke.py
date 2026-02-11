#!/usr/bin/env python3
"""
S M O K E — Claude Code Statusline
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
Dark, minimal, ember-accented. Form follows function.
Directory-first design for multi-instance awareness.

Line 1: 🔥 Model │ ~/clickable/path (fish-abbreviated when tight) ── branch +2 ~5 (repo)   #a1b2c3d4
Line 2:   ▰▰▰▰▰▰▰▱▱▱▱▱▱▱▱▱▱▱▱▱ 23% of 200k │ ⏱ 12m 34s │ $0.42 │ ↑156 ↓23

Requires: Python 3.9+, jq NOT required (pure Python JSON parsing)
Terminal: Best with iTerm2, Kitty, WezTerm, or Ghostty for clickable links
License: MIT — https://github.com/aismokeshow/statusline-starter
"""
import fcntl
import hashlib
import json
import os
import re
import struct
import subprocess
import sys
import tempfile
import termios
import time
from urllib.parse import quote

__version__ = "1.0.0"

# ━━ CLI flags ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "--version" in sys.argv:
    print(f"statusline-smoke {__version__}")
    sys.exit(0)

# ━━ Read JSON from Claude Code ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
if "--showcase" in sys.argv:
    import shutil as _shutil

    _home_dir = os.path.expanduser("~")
    _base = os.path.join(_home_dir, ".cache", "smoke-showcase")

    # Clean slate from any previous run
    if os.path.exists(_base):
        _shutil.rmtree(_base)

    # Stage 1: short path, no git repo
    _path_fresh = os.path.join(_base, "my-app")
    os.makedirs(_path_fresh)

    # Stages 2-5: deep path inside a controlled git repo
    _git_root = os.path.join(_base, "acme-corp-monorepo")
    _path_deep = os.path.join(_git_root, "apps", "dashboard", "src")
    os.makedirs(_path_deep)

    # Initialize git with controlled state
    _gr = lambda cmd: subprocess.run(
        cmd, capture_output=True, text=True, cwd=_git_root
    )
    _gr(["git", "init", "-b", "main"])
    _gr(["git", "config", "user.email", "dev@acme.com"])
    _gr(["git", "config", "user.name", "Dev"])
    _gr(["git", "remote", "add", "origin",
         "https://github.com/acme/monorepo.git"])

    # Commit baseline files
    for _fn in ["app.py", "config.py", "routes.py", "models.py", "utils.py"]:
        with open(os.path.join(_git_root, _fn), "w") as _f:
            _f.write(f"# {_fn}\n")
    _gr(["git", "add", "."])
    _gr(["git", "commit", "-m", "init"])

    # Stage 2 new files -> +2 staged
    for _fn in ["auth.py", "middleware.py"]:
        with open(os.path.join(_git_root, _fn), "w") as _f:
            _f.write(f"# {_fn}\n")
    _gr(["git", "add", "auth.py", "middleware.py"])

    # Modify 5 committed files -> ~5 unstaged
    for _fn in ["app.py", "config.py", "routes.py", "models.py", "utils.py"]:
        with open(os.path.join(_git_root, _fn), "a") as _f:
            _f.write("# updated\n")

    # Git state: main +2 ~5 (monorepo) -- same for stages 2-5

    # Clear git info caches for our paths
    for _p in [_path_fresh, _path_deep]:
        _h = hashlib.md5(_p.encode(), usedforsecurity=False).hexdigest()[:8]
        _cf = os.path.join(tempfile.gettempdir(), f"claude-smoke-git-{_h}")
        for _x in [_cf, _cf + ".tmp"]:
            try:
                os.unlink(_x)
            except FileNotFoundError:
                pass

    _stages = [
        ("1  FRESH START", {
            "model": {"display_name": "Opus 4.6"},
            "workspace": {"current_dir": _path_fresh},
            "cost": {},
            "context_window": {"context_window_size": 200000, "used_percentage": 2},
            "session_id": "a1b2c3d4",
        }),
        ("2  LIGHT WORK", {
            "model": {"display_name": "Sonnet 4.5"},
            "workspace": {"current_dir": _path_deep},
            "cost": {"total_cost_usd": 0.23, "total_duration_ms": 187000,
                     "total_lines_added": 42, "total_lines_removed": 8},
            "context_window": {"context_window_size": 200000, "used_percentage": 25},
            "session_id": "e5f6a7b8",
        }),
        ("3  DEEP SESSION", {
            "model": {"display_name": "Opus 4.6"},
            "workspace": {"current_dir": _path_deep},
            "cost": {"total_cost_usd": 1.37, "total_duration_ms": 847000,
                     "total_lines_added": 156, "total_lines_removed": 23},
            "context_window": {"context_window_size": 200000, "used_percentage": 55},
            "session_id": "c9d0e1f2",
            "transcript_path": "/tmp/smoke-transcript-demo.md",
        }),
        ("4  WARNING ZONE", {
            "model": {"display_name": "Opus 4.6"},
            "workspace": {"current_dir": _path_deep},
            "cost": {"total_cost_usd": 3.82, "total_duration_ms": 2340000,
                     "total_lines_added": 489, "total_lines_removed": 167},
            "context_window": {"context_window_size": 200000, "used_percentage": 68},
            "session_id": "a3b4c5d6",
            "transcript_path": "/tmp/smoke-transcript-demo.md",
            "vim": {"mode": "NORMAL"},
        }),
        ("5  CRITICAL", {
            "model": {"display_name": "Opus 4.6"},
            "workspace": {"current_dir": _path_deep},
            "cost": {"total_cost_usd": 7.14, "total_duration_ms": 4920000,
                     "total_lines_added": 812, "total_lines_removed": 341},
            "context_window": {"context_window_size": 200000, "used_percentage": 82},
            "session_id": "e7f8a9b0",
            "transcript_path": "/tmp/smoke-transcript-demo.md",
            "exceeds_200k_tokens": True,
            "agent": {"name": "researcher"},
        }),
    ]

    _self = os.path.abspath(sys.argv[0])
    print(flush=True)
    for _label, _data in _stages:
        print(f"\033[90m{'=' * 75}\033[0m", flush=True)
        print(f"\033[90m{_label}\033[0m", flush=True)
        print(f"\033[90m{'=' * 75}\033[0m", flush=True)
        _proc = subprocess.run(
            [sys.executable, _self],
            input=json.dumps(_data),
            capture_output=True, text=True,
            timeout=10,
        )
        sys.stdout.write(_proc.stdout)
        sys.stdout.flush()
        print(flush=True)

    # Cleanup
    _shutil.rmtree(_base, ignore_errors=True)
    sys.exit(0)

if "--preview" in sys.argv:
    data = {
        "model": {"display_name": "Opus 4.6"},
        "workspace": {"current_dir": os.getcwd()},
        "context_window": {"context_window_size": 200000, "used_percentage": 42},
        "cost": {
            "total_cost_usd": 1.37,
            "total_duration_ms": 847000,
            "total_lines_added": 156,
            "total_lines_removed": 23,
        },
        "session_id": "demo1234",
    }
else:
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        sys.exit(0)

# ━━ Extract Fields ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
model = data.get("model", {}).get("display_name", "?")
cwd = data.get("workspace", {}).get("current_dir") or data.get("cwd", "")
project_dir = data.get("workspace", {}).get("project_dir", "")
pct = int(data.get("context_window", {}).get("used_percentage") or 0)
ctx_size = data.get("context_window", {}).get("context_window_size") or 200000
cost = data.get("cost", {}).get("total_cost_usd") or 0
duration_ms = data.get("cost", {}).get("total_duration_ms") or 0
lines_added = data.get("cost", {}).get("total_lines_added") or 0
lines_removed = data.get("cost", {}).get("total_lines_removed") or 0
session_id = (data.get("session_id") or "")[:8]
transcript = data.get("transcript_path", "")
exceeds_200k = data.get("exceeds_200k_tokens", False)
vim_mode = (data.get("vim") or {}).get("mode", "")
agent_name = (data.get("agent") or {}).get("name", "")

# ━━ SMOKE Palette ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Grayscale backbone with ember accents
BOLD = "\033[1m"
RST = "\033[0m"
WHITE = "\033[97m"          # bright white — primary emphasis
SILVER = "\033[37m"         # light gray — secondary text
ASH = "\033[90m"            # dark gray — separators, muted info
EMBER = "\033[38;5;208m"    # bright orange — the signature accent
COAL = "\033[38;5;196m"     # red — critical/danger
SMOLDER = "\033[38;5;220m"  # warm yellow — warning zone
# Git colors retired — SMOKE palette covers everything.
# Staged/modified use SILVER/ASH; session diffs use EMBER/ASH.


# ━━ Helpers ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
def osc8(url, text):
    """OSC 8 clickable hyperlink (Cmd+click in iTerm2/Kitty/WezTerm/Ghostty)."""
    return f"\033]8;;{url}\a{text}\033]8;;\a"


# ━━ Terminal Width & Path Display ━━━━━━━━━━━━━━━━━━━━━━━━━
# Width-responsive paths: full when room, fish-abbreviated when tight.
# OSC 8 link always carries the full path — click to navigate.
_home = os.path.expanduser("~")


def term_width():
    """Terminal width via /dev/tty — works even with piped stdin/stdout."""
    try:
        with open("/dev/tty") as tty:
            res = fcntl.ioctl(tty.fileno(), termios.TIOCGWINSZ, b"\x00" * 8)
            return struct.unpack("hh", res[:4])[1]
    except Exception:
        return 120


def tilde(p):
    """Contract $HOME → ~."""
    return "~" + p[len(_home):] if (p == _home or p.startswith(_home + "/")) else p


def fish_path(p):
    """Bookend-abbreviate intermediate dirs (3…3), keep leaf full.
    ~/dev/aismokeshow_build_in_public/sub → ~/dev/ais…lic/sub
    """
    parts = p.split("/")
    if len(parts) <= 3:
        return p
    def abbrev(d):
        return (d[:3] + "…" + d[-3:]) if len(d) > 7 else d
    return "/".join([parts[0]] + [abbrev(d) for d in parts[1:-1]] + [parts[-1]])


COLS = term_width()


def smart_path(raw):
    """Width-responsive: full path with ~ when room, fish-abbreviated when tight."""
    contracted = tilde(raw)
    # Budget: terminal width minus ~90 chars for other line 1 segments + notifications
    budget = max(COLS - 90, 30)
    if len(contracted) <= budget:
        return contracted
    return fish_path(contracted)


def fmt_tokens(n):
    if n >= 1_000_000:
        return f"{n / 1_000_000:.1f}M"
    if n >= 1_000:
        return f"{int(n // 1_000)}k"
    return str(n)


def fmt_duration(ms):
    s = int(ms) // 1000
    m, s = divmod(s, 60)
    h, m = divmod(m, 60)
    if h > 0:
        return f"{h}h {m}m"
    if m > 0:
        return f"{m}m {s}s"
    return f"{s}s"


# ━━ Git Info (5s cache, per-directory) ━━━━━━━━━━━━━━━━━━━━━━
# Hash the cwd so each instance gets its own cache file
_dir_hash = hashlib.md5(cwd.encode(), usedforsecurity=False).hexdigest()[:8] if cwd else "default"
CACHE = os.path.join(tempfile.gettempdir(), f"claude-smoke-git-{_dir_hash}")
CACHE_TTL = 5


def git_info():
    stale = True
    if os.path.exists(CACHE):
        stale = (time.time() - os.path.getmtime(CACHE)) > CACHE_TTL

    if stale:
        try:
            subprocess.check_output(
                ["git", "rev-parse", "--git-dir"],
                stderr=subprocess.DEVNULL,
                cwd=cwd or None,
                timeout=3,
            )
            branch = subprocess.check_output(
                ["git", "branch", "--show-current"],
                text=True,
                stderr=subprocess.DEVNULL,
                cwd=cwd or None,
                timeout=3,
            ).strip()
            staged_out = subprocess.check_output(
                ["git", "diff", "--cached", "--numstat"],
                text=True,
                stderr=subprocess.DEVNULL,
                cwd=cwd or None,
                timeout=3,
            ).strip()
            modified_out = subprocess.check_output(
                ["git", "diff", "--numstat"],
                text=True,
                stderr=subprocess.DEVNULL,
                cwd=cwd or None,
                timeout=3,
            ).strip()
            staged_n = len(staged_out.split("\n")) if staged_out else 0
            modified_n = len(modified_out.split("\n")) if modified_out else 0

            # Remote URL for clickable repo link
            remote = ""
            try:
                remote = subprocess.check_output(
                    ["git", "remote", "get-url", "origin"],
                    text=True,
                    stderr=subprocess.DEVNULL,
                    cwd=cwd or None,
                    timeout=3,
                ).strip()
                # Convert SSH remote URLs to HTTPS for clickable links
                _m = re.match(r'^git@([^:]+):(.+?)(?:\.git)?$', remote)
                if _m:
                    remote = f"https://{_m.group(1)}/{_m.group(2)}"
                else:
                    remote = re.sub(r"\.git$", "", remote)
            except Exception:
                pass

            with open(CACHE + ".tmp", "w") as f:
                f.write(f"{branch}\t{staged_n}\t{modified_n}\t{remote}")
            os.rename(CACHE + ".tmp", CACHE)
        except Exception:
            try:
                with open(CACHE + ".tmp", "w") as f:
                    f.write("\t\t\t")
                os.rename(CACHE + ".tmp", CACHE)
            except Exception:
                pass

    try:
        with open(CACHE) as f:
            parts = f.read().rstrip('\n').split("\t", 3)
        if len(parts) >= 3:
            return (
                parts[0],
                int(parts[1] or 0),
                int(parts[2] or 0),
                parts[3] if len(parts) > 3 else "",
            )
    except Exception:
        pass
    return "", 0, 0, ""


branch, staged, modified, remote_url = git_info()


# ━━ Compact Threshold ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
# Computed early — used by both fire indicator and progress bar.
# Formula from reverse-engineered source (DecodeClaude, Jan 2026):
#   available = context_window_size - output_reserved
#   trigger   = available - 13000 (safety buffer)
# The 13K safety buffer is an internal constant (nx1=13000 in source).
_output_reserved = int(os.environ.get("CLAUDE_CODE_MAX_OUTPUT_TOKENS", "32000"))
_autocompact_override = os.environ.get("CLAUDE_AUTOCOMPACT_PCT_OVERRIDE", "")
_SAFETY_BUFFER = 13000

if _autocompact_override:
    # Direct override: percentage of available context (after output reservation)
    _override_pct = int(_autocompact_override)
    _available = ctx_size - _output_reserved
    compact_pct = (_available * _override_pct // 100) * 100 // ctx_size
else:
    # Default formula: (ctx_size - output_reserved - safety_buffer) / ctx_size
    compact_pct = max(0, (ctx_size - _output_reserved - _SAFETY_BUFFER) * 100 // ctx_size)


# ━━ BUILD LINE 1: Identity & Location ━━━━━━━━━━━━━━━━━━━━━━
# Fire indicator: always lit, escalates at compact threshold
if pct >= compact_pct or exceeds_200k:
    fire = "🔥🔥"                   # double fire — at compact threshold
else:
    fire = "🔥"                     # steady burn — signature element

# Model tag
model_seg = f"{BOLD}{WHITE}{model}{RST}"

# Agent name if running as agent
agent_seg = f" {ASH}[{RST}{EMBER}{agent_name}{RST}{ASH}]{RST}" if agent_name else ""

# Vim mode
vim_seg = f" {ASH}[{RST}{WHITE}{vim_mode}{RST}{ASH}]{RST}" if vim_mode else ""

# Directory — THE focal point. Display adapts to width; full path in OSC 8 link.
dir_display = smart_path(cwd) if cwd else "?"
dir_link = osc8(f"file://{quote(cwd, safe='/:@')}", dir_display) if cwd else "?"
dir_seg = f"{BOLD}{WHITE}{dir_link}{RST}"

# Drift: show origin only for true lateral drift, not subdirectory descent.
# When cwd is under project_dir, the path already contextualizes location.
drift_seg = ""
if project_dir and cwd and project_dir != cwd:
    if not cwd.startswith(project_dir + "/"):
        proj_name = os.path.basename(project_dir)
        drift_seg = f" {ASH}(from {proj_name}){RST}"

# Git segment
git_seg = ""
if branch:
    git_seg = f" {ASH}──{RST} {SILVER}{branch}{RST}"
    parts = []
    if staged > 0:
        parts.append(f"{SILVER}+{staged}{RST}")
    if modified > 0:
        parts.append(f"{ASH}~{modified}{RST}")
    if parts:
        git_seg += " " + " ".join(parts)
    # Clickable repo name
    if remote_url:
        repo_name = os.path.basename(remote_url.rstrip("/"))
        if repo_name:
            git_seg += f" {ASH}({RST}{osc8(remote_url, repo_name)}{ASH}){RST}"

# Session ID — distinguishes concurrent instances
session_seg = f" {ASH}#{session_id}{RST}" if session_id else ""

# Exceeds 200k warning
warn_seg = f" {COAL}[>200k]{RST}" if exceeds_200k else ""

line1 = f"{fire} {model_seg}{agent_seg}{vim_seg} {ASH}│{RST} {dir_seg}{drift_seg}{git_seg}{session_seg}{warn_seg}"


# ━━ BUILD LINE 2: Progress & Metrics ━━━━━━━━━━━━━━━━━━━━━━━
# Progress bar — 20 chars wide, ember-colored fill
# Compact threshold marker: shows where auto-compact fires on the bar.
BAR_W = 20
filled = min(pct * BAR_W // 100, BAR_W)
filled = max(filled, 0)
compact_pos = min(compact_pct * BAR_W // 100, BAR_W)

# Bar color shifts with heat — thresholds relative to compact point
if pct >= compact_pct:
    bar_color = COAL
elif pct >= compact_pct * 85 // 100:
    bar_color = SMOLDER
else:
    bar_color = EMBER

# Build bar with threshold marker at compact position
bar_chars = []
for i in range(BAR_W):
    if i < filled:
        bar_chars.append(f"{bar_color}▰{RST}")
    elif i == compact_pos and compact_pos < BAR_W:
        bar_chars.append(f"{ASH}│{RST}")
    else:
        bar_chars.append(f"{ASH}▱{RST}")
bar = "".join(bar_chars)

# Percentage — color matches bar
if pct >= compact_pct:
    pct_seg = f"{COAL}{pct}%{RST}"
elif pct >= compact_pct * 85 // 100:
    pct_seg = f"{SMOLDER}{pct}%{RST}"
else:
    pct_seg = f"{SILVER}{pct}%{RST}"

ctx_seg = f"{ASH}{fmt_tokens(ctx_size)}{RST}"
dur_seg = f"{ASH}⏱{RST} {SILVER}{fmt_duration(duration_ms)}{RST}"
cost_seg = f"{SILVER}${cost:.2f}{RST}"

# Lines changed
lines_seg = ""
if lines_added > 0 or lines_removed > 0:
    parts = []
    if lines_added > 0:
        parts.append(f"{EMBER}↑{lines_added}{RST}")
    if lines_removed > 0:
        parts.append(f"{ASH}↓{lines_removed}{RST}")
    lines_seg = f" {ASH}│{RST} " + " ".join(parts)

# Clickable transcript link (subtle, at the end)
transcript_seg = ""
if transcript:
    _transcript_url = f"file://{quote(transcript, safe='/:@')}"
    transcript_seg = f" {ASH}│{RST} {osc8(_transcript_url, f'{ASH}log{RST}')}"

line2 = f"  {bar} {pct_seg} {ASH}of{RST} {ctx_seg} {ASH}│{RST} {dur_seg} {ASH}│{RST} {cost_seg}{lines_seg}{transcript_seg}"


# ━━ Output ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
print(line1)
print(line2)
