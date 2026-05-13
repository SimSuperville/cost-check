# cost-check

A Claude Code slash command that shows token usage for your last message and current session, benchmarked against Claude plan limits — with a breakdown of how many tokens your MCP servers and Skills are consuming.

Run `/cost-check` and get an instant summary like:

```
⚡ /cost-check
──────────────────────────────────────────────────────────
                          INPUT    OUTPUT     TOTAL
  Last message            12.4k       847     13.2k
  Session (24 turns)     180.3k     8.1k    188.4k

  LAST MESSAGE  ── as % of 5-hr plan window
  Pro     ($20/mo  ~326k )  ░░░░░░░░░░░░░░░░░░░░    4.1%
  Max 5x  ($100/mo ~1.63M)  ░░░░░░░░░░░░░░░░░░░░    0.8%
  Max 20x ($200/mo ~6.52M)  ░░░░░░░░░░░░░░░░░░░░    0.2%

  SESSION TOTAL ── as % of 5-hr plan window
  Pro     ($20/mo  ~326k )  ████████████░░░░░░░░   57.8%
  Max 5x  ($100/mo ~1.63M)  ██░░░░░░░░░░░░░░░░░░   11.6%
  Max 20x ($200/mo ~6.52M)  ░░░░░░░░░░░░░░░░░░░░    2.9%

  MCP & SKILL INSIGHTS  ── est. tokens added to context
  MCP calls                  5 calls    ~13.9k tokens
    └─ claude_ai_n8n                       5 × ~13.9k
  (~31.1% of session input is MCP/Skill response payload)
──────────────────────────────────────────────────────────
```

Reads your local session JSONL files in `~/.claude/projects/`. No API calls, no authentication, no data leaves your machine.

## Install

In Claude Code:

```
/plugin marketplace add SimSuperville/cost-check
/plugin install cost-check
```

That's it. Run `/cost-check` to try it.

### Optional: skip the approval prompt

The first time you run `/cost-check`, Claude Code will ask permission to run the bundled Python script. Click **"Yes, and don't ask again for this exact command"** and you'll never see the prompt again.

Or add this to your `~/.claude/settings.json` upfront:

```json
{
  "permissions": {
    "allow": [
      "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cost-check.py)"
    ]
  }
}
```

## How it works

- Finds the most recently modified `*.jsonl` file in `~/.claude/projects/` (your current session).
- Parses assistant turns and sums `input_tokens` + `output_tokens` from the `usage` field.
- Excludes the trailing `/cost-check` invocation itself so it doesn't pollute the count.
- Compares against approximate per-plan 5-hour window limits.
- Detects MCP tool calls (`mcp__*`) and Skill calls, then estimates the tokens each one added to context by measuring the character length of their tool-result payloads (≈ chars / 4).

Plan limits are estimates based on community-observed quotas and Anthropic's official 5×/20× Max-to-Pro ratios — not authoritative caps. See [`docs/plan-limits.md`](docs/plan-limits.md) for the full sourcing and derivation. Anthropic does not publish exact Claude Code token budgets and can change them dynamically, so treat these as soft benchmarks.

## Manual install (no plugin)

If you don't want to use the plugin system, copy the two files directly:

1. `commands/cost-check.md` → `~/.claude/commands/cost-check.md`
2. `scripts/cost-check.py` → `~/.claude/scripts/cost-check.py`

Then update the path inside `cost-check.md` from `${CLAUDE_PLUGIN_ROOT}/scripts/cost-check.py` to `$HOME/.claude/scripts/cost-check.py`.

## License

MIT
