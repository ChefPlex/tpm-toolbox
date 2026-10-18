#!/usr/bin/env python3
"""
Shared plumbing for the template extractor and the draft generator.

Everything here is security- or correctness-relevant, which is why it lives in one place: a fix
to the tool boundary, the template schema or the coverage check reaches both scripts at once.

What this module enforces in code, rather than asking the model for:
- the tool boundary: no built-in tools, Slack read tools only, Slack write tools denied, and
  the tools the model actually called are checked after the run;
- the template schema, before a template is saved and again before it is used;
- a sensitive-data scan of extracted templates;
- source coverage, from the Slack reads the run was OBSERVED to make, not from the model's
  own coverage table;
- where generated output may be written.
"""

from __future__ import annotations

import json
import os
import platform
import re
import shutil
import subprocess
import tempfile
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

SCRIPT_DIR = Path(__file__).resolve().parent
DEFAULT_TEMPLATE_DIR = SCRIPT_DIR / ".canvas_templates"
# Generated drafts and manifests land here by default. The folder is gitignored.
DEFAULT_OUTPUT_DIR = SCRIPT_DIR / "drafts"

# Claude Code names MCP tools mcp__<server>__<tool>; a bare tool name matches no permission rule.
# The server part is whatever `claude mcp list` calls your Slack connection.
DEFAULT_SLACK_SERVER = "claude_ai_Slack"
CHANNEL_READ, CANVAS_READ = "slack_read_channel", "slack_read_canvas"
WRITE_TOOLS = ("slack_send_message", "slack_send_message_draft", "slack_schedule_message",
               "slack_create_canvas", "slack_update_canvas")
SAFE_TEMPLATE_NAME = re.compile(r"^[A-Za-z0-9_.-]+$")
SAFE_SERVER_NAME = re.compile(r"^[A-Za-z0-9_-]+$")

TEMPLATE_SCHEMA_VERSION = 1
MAX_FIELD_CHARS = 2000
MAX_LOOKBACK_DAYS = 90


# ── Names and the CLI ────────────────────────────────────────────────────────────────────────

def slack_server() -> str:
    server = os.environ.get("SLACK_MCP_SERVER", DEFAULT_SLACK_SERVER).strip()
    if not SAFE_SERVER_NAME.match(server):
        raise ValueError("SLACK_MCP_SERVER must use only letters, numbers, dashes, or underscores.")
    return server


def mcp_tool_names(server: str, tools: tuple[str, ...]) -> list[str]:
    if not SAFE_SERVER_NAME.match(server):
        raise ValueError("SLACK_MCP_SERVER must use only letters, numbers, dashes, or underscores.")
    return [f"mcp__{server}__{tool}" for tool in tools]


def validate_template_name(template_name: str) -> None:
    if not SAFE_TEMPLATE_NAME.match(template_name) or "/" in template_name or ".." in template_name:
        raise ValueError("Template name must use only letters, numbers, dots, dashes, or underscores.")


def resolve_claude_bin() -> str:
    candidates = [os.environ.get("CLAUDE_BIN"), shutil.which("claude")]
    for candidate in candidates:
        if not candidate:
            continue
        expanded = Path(candidate).expanduser()
        if expanded.exists() or shutil.which(candidate):
            return str(expanded if expanded.exists() else candidate)
    raise RuntimeError("Claude CLI not found. Set CLAUDE_BIN or make sure `claude` is on your PATH.")


def build_claude_command(prompt: str, read_tools: tuple[str, ...]) -> list[str]:
    """The Claude invocation, with the tool boundary set on the command line.

    - `--tools ""` removes every BUILT-IN tool (Bash, Edit, Write, WebFetch and the rest). A
      prompt injected through Slack content has no shell and no file access to reach for.
    - `--allowedTools` pre-approves the Slack read tools, and `--permission-mode dontAsk` makes
      the CLI DENY every tool that is not pre-approved instead of asking. Together they are the
      allowlist: a tool from another MCP server is refused, not just caught afterwards. The one
      exception is a tool your OWN Claude settings already allow; `--doctor` lists other servers.
    - `--disallowedTools` denies Slack's write tools whatever your own settings allow.
    - For a strict boundary, set SLACK_MCP_CONFIG to a JSON file that defines only your Slack
      server. The run then loads that file alone (`--strict-mcp-config`).
    After the run, `tool_surface_problems()` checks which tools were actually called.
    """
    cmd: list[str] = []
    if platform.system() == "Darwin" and os.environ.get("NO_CAFFEINATE") != "1" and shutil.which("caffeinate"):
        cmd.extend(["caffeinate", "-s"])
    cmd.append(resolve_claude_bin())
    server = slack_server()
    cmd.extend(["--tools", ""])
    cmd.extend(["--permission-mode", "dontAsk"])
    cmd.extend(["--allowedTools", ",".join(mcp_tool_names(server, read_tools))])
    cmd.extend(["--disallowedTools", ",".join(mcp_tool_names(server, WRITE_TOOLS))])
    mcp_config = os.environ.get("SLACK_MCP_CONFIG", "").strip()
    if mcp_config:
        cmd.extend(["--mcp-config", str(Path(mcp_config).expanduser()), "--strict-mcp-config"])
    cmd.extend(["--output-format", "stream-json", "--verbose"])
    cmd.extend(["-p", prompt])
    return cmd


# ── Running Claude and reading what it actually did ──────────────────────────────────────────

@dataclass
class ToolCall:
    name: str
    input: dict[str, Any]
    is_error: bool = False
    result_text: str = ""


@dataclass
class RunResult:
    returncode: int
    text: str = ""
    is_error: bool = False
    stderr: str = ""
    available_tools: list[str] = field(default_factory=list)
    mcp_servers: dict[str, str] = field(default_factory=dict)
    calls: list[ToolCall] = field(default_factory=list)
    parsed: bool = False


def _result_text(content: Any) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(c.get("text", "") for c in content if isinstance(c, dict))
    return ""


def parse_stream(stdout: str, returncode: int = 0, stderr: str = "") -> RunResult:
    """Read Claude's stream-json output into what the run was offered, called and returned.

    `parsed` is False when no `result` event arrived; the run is then treated as failed, never
    as an empty success."""
    run = RunResult(returncode=returncode, stderr=stderr)
    by_id: dict[str, ToolCall] = {}
    for line in (stdout or "").splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if not isinstance(event, dict):
            continue
        kind = event.get("type")
        if kind == "system" and event.get("subtype") == "init":
            run.available_tools = [t for t in event.get("tools") or [] if isinstance(t, str)]
            run.mcp_servers = {re.sub(r"[^A-Za-z0-9_]", "_", str(s.get("name"))): str(s.get("status"))
                               for s in event.get("mcp_servers") or [] if isinstance(s, dict)}
        elif kind in ("assistant", "user"):
            content = (event.get("message") or {}).get("content")
            for block in content if isinstance(content, list) else []:
                if not isinstance(block, dict):
                    continue
                if block.get("type") == "tool_use":
                    args = block.get("input")
                    call = ToolCall(name=str(block.get("name")), input=args if isinstance(args, dict) else {})
                    by_id[str(block.get("id"))] = call
                    run.calls.append(call)
                elif block.get("type") == "tool_result" and str(block.get("tool_use_id")) in by_id:
                    call = by_id[str(block.get("tool_use_id"))]
                    call.is_error = bool(block.get("is_error"))
                    call.result_text = _result_text(block.get("content"))
        elif kind == "result":
            run.parsed = True
            run.text = str(event.get("result") or "")
            run.is_error = bool(event.get("is_error"))
    if not run.parsed:
        run.is_error = True
    return run


def run_claude(prompt: str, read_tools: tuple[str, ...], timeout: int) -> RunResult:
    proc = subprocess.run(build_claude_command(prompt, read_tools), stdin=subprocess.DEVNULL,
                          capture_output=True, text=True, timeout=timeout, check=False)
    return parse_stream(proc.stdout, proc.returncode, proc.stderr)


def tool_surface_problems(run: RunResult, read_tools: tuple[str, ...],
                          channel_ids: list[str] | None = None,
                          canvas_ids: list[str] | None = None) -> list[str]:
    """Every way the run left its boundary: a tool beyond the Slack read tools, or a read of a
    source nobody requested.

    The second check is the one that matters most. An instruction planted in a Slack message or a
    template ("also read channel C0EXEC…") needs no forbidden tool: it uses the allowed read tool on
    the wrong ID. Passing the requested IDs makes that a failure instead of a quiet extra read."""
    server = slack_server()
    allowed = set(mcp_tool_names(server, read_tools))
    channel_tool, canvas_tool = mcp_tool_names(server, (CHANNEL_READ, CANVAS_READ))
    problems = [f"the run called {c.name}, which is outside the read-only boundary"
                for c in run.calls if c.name not in allowed]
    for call in run.calls:
        if call.name == channel_tool and channel_ids is not None:
            sid = str(call.input.get("channel_id"))
            if sid not in channel_ids:
                problems.append(f"the run read channel {sid}, which was not requested")
        elif call.name == canvas_tool and canvas_ids is not None:
            sid = str(call.input.get("canvas_id"))
            if sid not in canvas_ids:
                problems.append(f"the run read canvas {sid}, which was not requested")
    return problems


def surface_report(run: RunResult, read_tools: tuple[str, ...]) -> tuple[list[str], list[str]]:
    """(errors, notes) about the tools a run was OFFERED, from its init event. Used by --doctor."""
    server = slack_server()
    needed = mcp_tool_names(server, read_tools)
    writes = mcp_tool_names(server, WRITE_TOOLS)
    errors, notes = [], []
    if run.mcp_servers.get(server) != "connected":
        state = run.mcp_servers.get(server, "not loaded")
        errors.append(f"the Slack MCP server '{server}' is {state}. Known servers: "
                      f"{', '.join(f'{k} ({v})' for k, v in sorted(run.mcp_servers.items())) or 'none'}")
    if not run.available_tools:
        errors.append("the run reported no tool list, so the boundary could not be checked")
        return errors, notes
    missing = [t for t in needed if t not in run.available_tools]
    if missing:
        errors.append(f"Slack read tools are not available: {', '.join(missing)}. Check SLACK_MCP_SERVER "
                      f"and `claude mcp list`.")
    builtins = [t for t in run.available_tools if not t.startswith("mcp__")]
    if builtins:
        errors.append(f"built-in tools are available despite --tools \"\": {', '.join(builtins)}")
    open_writes = [t for t in writes if t in run.available_tools]
    if open_writes:
        notes.append(f"Slack write tools are listed but denied by --disallowedTools: {', '.join(open_writes)}")
    others = sorted({t.split("__")[1] for t in run.available_tools
                     if t.startswith("mcp__") and t.split("__")[1] != server})
    if others:
        notes.append(f"other MCP servers are also loaded ({', '.join(others)}). Set SLACK_MCP_CONFIG "
                     f"for a Slack-only session.")
    return errors, notes


# ── The template schema ──────────────────────────────────────────────────────────────────────

# A Slack tool name, as a planted instruction would write it: `mcp__…` or `slack_<verb>_…`.
# `{{slack_handle}}`-style placeholders are removed before this runs, so they never match.
_TOOL_NAME = re.compile(r"mcp__|\bslack_(?:read|send|schedule|create|update|search|delete|post)\w*", re.I)
_PLACEHOLDER = re.compile(r"\{\{[^{}]*\}\}")
_RISK_SECTION = re.compile(r"risk|blocker|issue|escalat|concern|red flag|watch|impediment|threat|"
                           r"dependenc|ask", re.I)
# Fields the wrapper sets itself, so they are not template text.
_WRAPPER_FIELDS = ("$.template_name", "$.source_canvas_id")


def _strings(value: Any, path: str = "$"):
    """Every string in the template, KEYS included: an emoji key is pasted into the prompt too."""
    if isinstance(value, str):
        yield path, value
    elif isinstance(value, dict):
        for k, v in value.items():
            yield f"{path}.<key {k}>", str(k)
            yield from _strings(v, f"{path}.{k}")
    elif isinstance(value, list):
        for i, v in enumerate(value):
            yield from _strings(v, f"{path}[{i}]")


def validate_template(template: Any) -> list[str]:
    """Every reason this template is unsafe or unusable to generate from. [] means valid.

    Checked when a template is extracted (it is not saved if this fails) and again when the
    generator loads it (a hand-edited file gets the same check)."""
    if not isinstance(template, dict):
        return ["the template is not a JSON object"]
    errors: list[str] = []
    version = template.get("schema_version")
    if version is not None and version != TEMPLATE_SCHEMA_VERSION:
        errors.append(f"schema_version {version!r} is not {TEMPLATE_SCHEMA_VERSION}, the version this "
                      f"tool reads. Re-extract the template.")
    sections = template.get("sections")
    if not isinstance(sections, list) or not sections:
        errors.append("`sections` must be a non-empty list")
        sections = []
    names: list[str] = []
    for i, section in enumerate(sections):
        if not isinstance(section, dict):
            errors.append(f"sections[{i}] is not an object")
            continue
        name = section.get("name")
        if not isinstance(name, str) or not name.strip():
            errors.append(f"sections[{i}] has no name")
            continue
        names.append(name.strip().lower())
        if "required" in section and not isinstance(section["required"], bool):
            errors.append(f"sections[{i}].required must be true or false")
        if "subsections" in section and not isinstance(section["subsections"], list):
            errors.append(f"sections[{i}].subsections must be a list")
    if len(names) != len(set(names)):
        errors.append("section names must be unique")
    if sections and not any(_RISK_SECTION.search(n) for n in names):
        errors.append("no risks / blockers section (risks, blockers, issues, concerns, red flags, watch "
                      "list, dependencies or asks): a status report without one reads healthy by omission")

    for key, kind in (("data_sources", dict), ("formatting_rules", dict), ("emoji_dictionary", dict),
                      ("review_checklist", list), ("stakeholder_pattern", str), ("title_format", str)):
        if key in template and not isinstance(template[key], kind):
            errors.append(f"`{key}` must be a {kind.__name__}")
    sources = template.get("data_sources")
    if isinstance(sources, dict) and "lookback_days" in sources:
        days = sources["lookback_days"]
        if isinstance(days, bool) or not isinstance(days, int) or not 1 <= days <= MAX_LOOKBACK_DAYS:
            errors.append(f"data_sources.lookback_days must be a whole number from 1 to {MAX_LOOKBACK_DAYS}")

    for path, text in _strings(template):
        if len(text) > MAX_FIELD_CHARS:
            errors.append(f"{path} is longer than {MAX_FIELD_CHARS} characters")
        hit = None if path in _WRAPPER_FIELDS else _TOOL_NAME.search(_PLACEHOLDER.sub("", text))
        if hit:
            # Template text is pasted into the generator's prompt. A tool name inside it is an
            # instruction written into the canvas, not formatting guidance. A paraphrased one
            # ("also read channel C0…") is caught at run time instead: an unrequested read fails.
            errors.append(f"{path} names a tool ({hit.group(0)})")
    return errors


_SENSITIVE = [
    ("link", re.compile(r"https?://\S+", re.I)),
    ("email address", re.compile(r"\b[\w.+-]+@[\w-]+\.[\w.-]+\b")),
    ("Slack mention", re.compile(r"<[@#!][A-Z0-9|^>]+>")),
    # A real Slack ID always carries a digit. Requiring one keeps all-caps headings such as
    # COMPLETED or DEPENDENCIES from reading as IDs.
    ("Slack ID", re.compile(r"\b[CDGUWF](?=[A-Z0-9]*\d)[A-Z0-9]{8,10}\b")),
]


def sensitive_findings(template: dict[str, Any]) -> list[tuple[str, str, str]]:
    """(path, kind, excerpt) for every value that looks like real data rather than a placeholder.

    The extraction prompt ASKS for placeholders; this checks that it got them. Terms you know
    are confidential (a codename, a customer) go in SENSITIVE_TERMS, comma-separated."""
    terms = [t.strip() for t in os.environ.get("SENSITIVE_TERMS", "").split(",") if t.strip()]
    found = []
    for path, text in _strings(template):
        if path in _WRAPPER_FIELDS:
            continue
        for kind, rx in _SENSITIVE:
            m = rx.search(text)
            if m:
                found.append((path, kind, m.group(0)[:60]))
        for term in terms:
            if term.lower() in text.lower():
                found.append((path, "listed sensitive term", term))
    return found


# ── Coverage: what the run was OBSERVED to read ──────────────────────────────────────────────

_NULLISH = {"", "null", "none", "false", "0"}

# ⛔ Both readers below look ONLY at structured fields of a JSON result: top level and
# `response_metadata`. Never at free text. A read result contains the channel's messages, which
# anyone in the channel wrote, so searching the text for "next_cursor: null" or "not_in_channel"
# would let a posted message make a cut-off channel look complete, or a good read look failed.


def _json(result_text: str) -> dict[str, Any] | None:
    try:
        data = json.loads(result_text)
    except (TypeError, ValueError):
        return None
    return data if isinstance(data, dict) else None


def _slack_error(result_text: str) -> str | None:
    """A Slack error the read returned as structured content (`ok: false` / `error`), or None.
    Such a read counts as failed, like one whose tool result was flagged `is_error`."""
    data = _json(result_text)
    if data is not None and (data.get("ok") is False or data.get("error")):
        return str(data.get("error") or "ok: false")
    return None


def page_has_more(result_text: str) -> bool | None:
    """Does this channel page say more messages remain? True, False, or None for UNKNOWN.

    Three answers on purpose. A JSON page with a non-empty `next_cursor` (top level or in
    `response_metadata`) or `has_more: true` has more; an empty or null cursor, or an empty page,
    has none. Anything else, including a plain-text result, is UNKNOWN: never assumed to be the
    last page, and never read from text a channel member could have written. Whether your Slack
    connector returns these fields is what `--doctor --doctor-channel` checks."""
    if not (result_text or "").strip():
        return False
    data = _json(result_text)
    if data is None:
        return None
    meta = data.get("response_metadata")
    meta = meta if isinstance(meta, dict) else {}
    for source in (data, meta):
        if "next_cursor" in source:
            return str(source["next_cursor"]).strip().lower() not in _NULLISH
    if "has_more" in data:
        return bool(data["has_more"])
    return None


def _table_ids(draft: str) -> set[str]:
    """IDs listed in the draft's Source Coverage table, if it has one."""
    idx = draft.lower().find("source coverage")
    if idx == -1:
        return set()
    ids = set()
    for line in draft[idx:].splitlines():
        if line.strip().startswith("|"):
            ids.update(re.findall(r"\b[CDGF][A-Z0-9]{8,10}\b", line))
    return ids


def coverage_manifest(run: RunResult, channel_ids: list[str], canvas_ids: list[str],
                      max_pages: int) -> dict[str, Any]:
    """The evidence record for a draft: every requested source, and what the run did with it.

    `read`, `pages` and `truncated` come from the tool calls the run was observed to make. The
    model's own Source Coverage table is recorded beside them as a claim, never as the evidence.

    Two lists, because they are different claims:
      problems   something was definitely missed: a source not read, a read that returned a Slack
                 error, a channel with more messages left, a source missing from the draft's table
      uncertain  a channel was read, but its last page carried no signal saying whether more
                 messages remain. Not assumed complete, not assumed truncated: reported.
    `complete` means no problems. `verified_complete` also means nothing uncertain; --strict uses it."""
    server = slack_server()
    channel_tool, canvas_tool = mcp_tool_names(server, (CHANNEL_READ, CANVAS_READ))
    in_table = _table_ids(run.text)
    sources = []
    for sid, kind, tool, key in ([(c, "channel", channel_tool, "channel_id") for c in channel_ids]
                                 + [(c, "canvas", canvas_tool, "canvas_id") for c in canvas_ids]):
        calls = [c for c in run.calls if c.name == tool and str(c.input.get(key)) == sid]
        failed = [c for c in calls if c.is_error or _slack_error(c.result_text)]
        ok = [c for c in calls if c not in failed]
        entry: dict[str, Any] = {"id": sid, "type": kind, "read": bool(ok), "calls": len(calls),
                                 "errors": len(failed), "in_draft_table": sid in in_table}
        if failed:
            entry["error_detail"] = sorted({_slack_error(c.result_text) or "tool error" for c in failed})
        if kind == "channel":
            more = page_has_more(ok[-1].result_text) if ok else None
            entry["pages"] = len(ok)
            entry["truncated"] = "unknown" if more is None else more
            entry["page_cap_hit"] = len(ok) >= max_pages and more is True
        sources.append(entry)
    problems, uncertain = [], []
    for s in sources:
        if not s["read"]:
            detail = f" ({s['errors']} failed call(s): {', '.join(s.get('error_detail', []))})" if s["errors"] else ""
            problems.append(f"{s['type']} {s['id']} was not read{detail}")
        elif s.get("truncated") is True:
            problems.append(f"channel {s['id']} has more messages than were read ({s['pages']} page(s))")
        elif s.get("truncated") == "unknown":
            uncertain.append(f"channel {s['id']}: its last page did not say whether more messages remain")
        if not s["in_draft_table"]:
            problems.append(f"{s['type']} {s['id']} is missing from the draft's Source Coverage table")
    return {"schema": 2, "complete": not problems, "verified_complete": not problems and not uncertain,
            "problems": problems, "uncertain": uncertain, "sources": sources,
            "tools_called": sorted({c.name for c in run.calls})}


# ── Output ───────────────────────────────────────────────────────────────────────────────────

def tracked_output_problem(path: Path) -> str | None:
    """A reason not to write generated text here, or None.

    Generated drafts carry program details from private Slack channels. Written inside a git
    working tree and not ignored, one `git add .` publishes them."""
    folder = path.parent if path.parent.exists() else next((p for p in path.parents if p.exists()), None)
    if folder is None or not shutil.which("git"):
        return None
    inside = subprocess.run(["git", "-C", str(folder), "rev-parse", "--is-inside-work-tree"],
                            capture_output=True, text=True, check=False)
    if inside.returncode != 0 or inside.stdout.strip() != "true":
        return None
    ignored = subprocess.run(["git", "-C", str(folder), "check-ignore", "-q", str(path)],
                             capture_output=True, check=False)
    if ignored.returncode == 0:
        return None
    return (f"{path} is inside a git repository and is NOT ignored, so `git add .` would commit it. "
            f"Write under {DEFAULT_OUTPUT_DIR} (ignored), or pass --allow-tracked-output.")


def write_text(path: Path, content: str) -> None:
    """Write atomically: a crash or a full disk leaves the old file or none, never half a file."""
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(dir=path.parent, prefix=f".{path.name}.", suffix=".tmp")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as fh:
            fh.write(content)
        os.replace(tmp, path)
    except BaseException:
        Path(tmp).unlink(missing_ok=True)
        raise
