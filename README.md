# cost-check

  A Claude Code slash command that shows token usage for your last message and current session, benchmarked against Claude plan limits.

  Run `/cost-check` and get an instant summary like:

  ⚡ /cost-check
  ──────────────────────────────────────────────────────────
                            INPUT    OUTPUT     TOTAL
    Last message            12.4k       847     13.2k
    Session (24 turns)     180.3k     8.1k    188.4k

    LAST MESSAGE  ── as % of 5-hr plan window
    Pro     ($20/mo   ~44k )  ██████░░░░░░░░░░░░░░   30.1%
    Max 5x  ($100/mo  ~88k )  ███░░░░░░░░░░░░░░░░░   15.0%
    Max 20x ($200/mo ~220k )  █░░░░░░░░░░░░░░░░░░░    6.0%

    SESSION TOTAL ── as % of 5-hr plan window
    ...

  Reads your local session JSONL files in `~/.claude/projects/`. No API calls, no authentication, no data leaves your machine.

  ## Install

  In Claude Code:

  /plugin marketplace add /cost-check
  /plugin install cost-check

  That's it. Run `/cost-check` to try it.

  ### Optional: skip the approval prompt

  The first time you run `/cost-check`, Claude Code will ask permission to run the bundled Python script. Click **"Yes, and don't ask again for this exact command"** and you'll never see the
  prompt again.

  Or add this to your `~/.claude/settings.json` upfront:

  ```json
  {
    "permissions": {
      "allow": [
        "Bash(python3 ${CLAUDE_PLUGIN_ROOT}/scripts/cost-check.py)"
      ]
    }
  }

  How it works

  - Finds the most recently modified *.jsonl file in ~/.claude/projects/ (your current session).
  - Parses assistant turns and sums input_tokens + output_tokens from the usage field.
  - Excludes the trailing /cost-check invocation itself so it doesn't pollute the count.
  - Compares against approximate per-plan 5-hour window limits.

  Plan limits are estimates based on observed quotas — not official numbers.

  Manual install (no plugin)

  If you don't want to use the plugin system, copy the two files directly:

  1. commands/cost-check.md → ~/.claude/commands/cost-check.md
  2. scripts/cost-check.py → ~/.claude/scripts/cost-check.py

  Then update the path inside cost-check.md from ${CLAUDE_PLUGIN_ROOT}/scripts/cost-check.py to $HOME/.claude/scripts/cost-check.py.
