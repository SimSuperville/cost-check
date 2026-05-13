# Claude Code Five-Hour Token Budget Estimates for Consumer Plans

**Date:** May 13, 2026
**Scope:** This document estimates the total input-plus-output token budget that a user can realistically consume in a single rolling five-hour usage window when using **Claude Code** through Anthropic consumer subscriptions: **Claude Pro**, **Claude Max 5x**, and **Claude Max 20x**. These are the values hardcoded in `scripts/cost-check.py`.

## Recommended Hardcoded Values

The following values are the best current estimates to hardcode in a token-usage tool as of May 13, 2026. They are not official quotas; Anthropic does not publish exact token budgets for consumer Claude Code five-hour windows.

| Plan | Recommended 5-Hour Budget | Source Quality | Confidence | Rationale |
|---|---:|---|---|---|
| **Claude Pro** | **326,000** tokens | Inferred | Medium | Derived from a Max 5x community datapoint, Anthropic's official 5x ratio, and the May 6, 2026 doubling announcement. |
| **Claude Max 5x** | **1,630,000** tokens | Community-observed + inferred | Medium-high | Based on a recent Reddit report of 766.1k tokens equaling 94% of a Max 5x five-hour session, doubled after Anthropic's May 6 change. |
| **Claude Max 20x** | **6,520,000** tokens | Inferred | Medium | Derived from the Pro estimate using Anthropic's official 20x ratio; sanity-checked against a separate 6.44M-token Team Premium measurement. |

> **Disclaimer:** Anthropic does not disclose exact Claude Code quotas and can change them dynamically, so these are best-effort May 2026 estimates, not guaranteed limits.

## Official Source Findings

Anthropic's official documentation confirms the structure of Claude Code usage limits, but it does **not** publish exact token budgets for consumer plans. The support article on using Claude Code with Pro and Max states that both plans share usage limits across Claude and Claude Code, meaning activity in both products counts against the same usage pool.[1] A separate support article on extra usage confirms that session limits reset every five hours and that extra usage applies to Pro, Max 5x, and Max 20x plans.[2]

Anthropic's Max plan support article provides the most important official conversion ratios. It states that **Max 5x provides five times more usage per session than Pro**, while **Max 20x provides twenty times more usage per session than Pro**.[3] These ratios are used in the estimates below.

On May 6, 2026, Anthropic announced that it was **doubling Claude Code's five-hour rate limits** for Pro, Max, Team, and seat-based Enterprise plans, and removing the peak-hours limit reduction for Pro and Max accounts.[4] This announcement is critical because the strongest community token-count datapoints located during research predate May 6, so they must be adjusted upward by a factor of two.

| Official Claim | Source | Published or Updated | Relevance |
|---|---|---:|---|
| Claude Code usage is shared with Claude usage under Pro and Max. | Anthropic Support: "Use Claude Code with your Pro or Max plan"[1] | Updated over a week before May 13, 2026 | Confirms Claude Code consumes the same subscription usage pool. |
| Session limits reset every five hours. | Anthropic Support: "Manage extra usage for paid Claude plans"[2] | Updated the week of May 13, 2026 | Confirms rolling five-hour reset behavior. |
| Max 5x is 5× Pro; Max 20x is 20× Pro per session. | Anthropic Support: "What is the Max plan?"[3] | April 7, 2026 | Provides official plan multipliers. |
| Claude Code five-hour limits doubled for Pro and Max. | Anthropic News: "Higher usage limits for Claude and a compute deal with SpaceX"[4] | May 6, 2026 | Requires doubling pre-May-6 observations. |

## Community and Indirect Evidence

The strongest current numeric datapoint comes from a recent r/ClaudeCode post titled "94% of a 5x Max 5-hour session usage is 766.1k tokens." The user reported that a **Max 5x** account had consumed **766.1k tokens** while showing **94%** of the five-hour session used.[5] The post was approximately 22 days old when reviewed on May 13, 2026, placing it before Anthropic's May 6 limit-doubling announcement.

Using that observation, the implied pre-doubling Max 5x budget is:

```
766100 / 0.94 = 815000 tokens
```

Because Anthropic officially doubled Claude Code five-hour limits on May 6, the post-doubling Max 5x estimate becomes:

```
815000 * 2 = 1630000 tokens
```

Anthropic's official Max ratios then imply the Pro and Max 20x budgets:

```
Pro = 1630000 / 5 = 326000 tokens
Max 20x = 326000 * 20 = 6520000 tokens
```

A second useful datapoint is a Zenn article that measured Claude Code CLI usage on a **Claude Team Plan Premium Seat** using Opus. The author reported that **3,543,683 tokens** increased the five-hour usage rate by **55 percentage points**, implying a full five-hour window of approximately **6,443,060 tokens**.[6] This measurement was taken on May 5, 2026, before Anthropic's May 6 increase, and it is not a consumer Max 20x measurement. Nevertheless, it is directionally useful because it lands close to the **6.52M-token** Max 20x estimate derived from the Max 5x community datapoint.

Additional reports confirm that users on Max 20x can hit a five-hour Claude Code limit, especially with Opus and high thinking settings, but the reports reviewed did not include exact token counts.[7]

| Source | Date or Recency | Reported Plan | Reported Usage | Source Quality | Usefulness |
|---|---:|---|---:|---|---|
| Reddit r/ClaudeCode: "94% of a 5x Max 5-hour session usage is 766.1k tokens"[5] | About Apr. 21, 2026 | Max 5x | 766.1k tokens = 94% | Community-observed | Strongest consumer-plan numeric datapoint. |
| Zenn: "Estimating Claude Code's 5-Hour Usage Limit"[6] | Published May 7, 2026; measured May 5, 2026 | Team Premium Seat | 3,543,683 tokens = 55%; inferred 6.44M full window | Community-measured / indirect | Useful sanity check, not a consumer Max source. |
| Reddit r/ClaudeCode: "Hit 5 hour limit on Max 20x"[7] | About Mar. 30, 2026 | Max 20x | 100% session used; no token total | Community-observed | Confirms Max 20x five-hour cap behavior, but not numeric. |
| GitHub usage monitor repository constants[8] | Source inspected May 13, 2026 | Pro, Max5, Max20 | Pro 19k, Max5 88k, Max20 220k in source constants | Community/tool-internal | Low confidence for current hardcoding; conflicts with recent observed data. |

## Source Quality Assessment

The **official** sources are reliable for the existence of five-hour windows, the Max-to-Pro ratios, shared Claude/Claude Code usage, and the May 6 doubling. They are not sufficient to compute exact token budgets because Anthropic does not state token counts.

The **community-observed** Max 5x datapoint is the best available consumer-plan token-count evidence because it includes a plan tier, a percentage consumed, and a token total. Its main weakness is that it is a single user report and predates Anthropic's May 6 change, requiring adjustment.

The **inferred** values are mathematically straightforward but depend on two assumptions: first, that the reported 766.1k-at-94% Max 5x observation reflected the relevant subscription limit rather than a transient bug or model-specific throttle; second, that Anthropic's May 6 doubling applied cleanly as a 2× multiplier to that same budget. The official announcement supports the second assumption, but Anthropic may still adjust limits dynamically.

## Final Recommendation

For a Claude Code token-usage tool that compares a user's current session consumption against rolling five-hour consumer-plan windows, the recommended hardcoded integer values are:

```json
{
  "pro": 326000,
  "max_5x": 1630000,
  "max_20x": 6520000
}
```

These should be treated as **soft estimates**, not authoritative caps. A robust tool should expose them as configurable defaults, include a disclaimer, and ideally allow users to calibrate against their own observed `/status`, usage-bar, or local token-accounting data.

## References

[1]: https://support.claude.com/en/articles/11145838-use-claude-code-with-your-pro-or-max-plan "Use Claude Code with your Pro or Max plan"
[2]: https://support.claude.com/en/articles/12429409-manage-extra-usage-for-paid-claude-plans "Manage extra usage for paid Claude plans"
[3]: https://support.claude.com/en/articles/11049741-what-is-the-max-plan "What is the Max plan?"
[4]: https://www.anthropic.com/news/higher-limits-spacex "Higher usage limits for Claude and a compute deal with SpaceX"
[5]: https://www.reddit.com/r/ClaudeCode/comments/1ssd676/94_of_a_5x_max_5hour_session_usage_is_7661k/ "94% of a 5x Max 5-hour session usage is 766.1k tokens"
[6]: https://zenn.dev/sato_shogidemo/articles/claude-code-usage-limit-token-estimate?locale=en "Estimating Claude Code's 5-Hour Usage Limit"
[7]: https://www.reddit.com/r/ClaudeCode/comments/1s7w3no/hit_5_hour_limit_on_max_20x/ "Hit 5 hour limit on Max 20x"
[8]: https://github.com/Maciek-roboblog/Claude-Code-Usage-Monitor "Claude Code Usage Monitor"
