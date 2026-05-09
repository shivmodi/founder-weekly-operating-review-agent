from __future__ import annotations

import json
from pathlib import Path

from .analysis import money, percent


def write_outputs(analysis: dict, out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    (out_dir / "weekly_operating_review.md").write_text(
        render_weekly_review(analysis), encoding="utf-8"
    )
    (out_dir / "investor_safe_update.md").write_text(
        render_investor_update(analysis), encoding="utf-8"
    )
    (out_dir / "team_asks.md").write_text(render_team_asks(analysis), encoding="utf-8")
    (out_dir / "next_week_plan.md").write_text(
        render_next_week_plan(analysis), encoding="utf-8"
    )
    (out_dir / "analysis.json").write_text(
        json.dumps(analysis, indent=2), encoding="utf-8"
    )


def render_weekly_review(analysis: dict) -> str:
    latest = analysis["latest"]
    deltas = analysis["deltas"]
    lines = [
        f"# Weekly Operating Review: {latest['week']}",
        "",
        f"## Headline",
        "",
        analysis["headline"],
        "",
        "## Metrics Snapshot",
        "",
        "| Metric | Latest | Change |",
        "|---|---:|---:|",
        f"| MRR | {money(latest['mrr'])} | {percent(deltas['mrr_growth'])} |",
        f"| Net New MRR | {money(latest['new_mrr'] + latest['expansion_mrr'] - latest['churn_mrr'])} | {percent(deltas['net_new_mrr_growth'])} |",
        f"| Activation Rate | {percent(latest['activation_rate'])} | {percent(deltas['activation_delta'])} pts |",
        f"| Pipeline Value | {money(latest['pipeline_value'])} | {percent(deltas['pipeline_growth'])} |",
        f"| Runway | {latest['runway_months']:.1f} months | n/a |",
        f"| Support Tickets Open | {latest['support_tickets_open']} | {percent(deltas['support_ticket_growth'])} |",
        f"| NPS | {latest['nps']:.0f} | n/a |",
        "",
        "## Risks",
        "",
    ]
    if analysis["risks"]:
        for risk in analysis["risks"]:
            lines.append(
                f"- **{risk['severity'].title()} - {risk['area'].title()}:** {risk['risk']} {risk['why_it_matters']}"
            )
    else:
        lines.append("- No material operating risk triggered this week.")

    lines.extend(["", "## Priorities", ""])
    lines.extend(
        f"{index}. {priority}"
        for index, priority in enumerate(analysis["priorities"], start=1)
    )
    lines.extend(["", "## Team Asks", ""])
    lines.extend(f"- **{ask['team']}:** {ask['ask']}" for ask in analysis["team_asks"])
    lines.extend(
        ["", "## Investor-Safe Summary", "", analysis["investor_safe_summary"], ""]
    )
    return "\n".join(lines)


def render_investor_update(analysis: dict) -> str:
    latest = analysis["latest"]
    return "\n".join(
        [
            f"# Investor Update Draft: {latest['week']}",
            "",
            analysis["investor_safe_summary"],
            "",
            "## Current Focus",
            "",
            *[f"- {priority}" for priority in analysis["priorities"][:3]],
            "",
        ]
    )


def render_team_asks(analysis: dict) -> str:
    latest = analysis["latest"]
    lines = [f"# Team Asks: {latest['week']}", ""]
    lines.extend(f"- **{ask['team']}:** {ask['ask']}" for ask in analysis["team_asks"])
    lines.append("")
    return "\n".join(lines)


def render_next_week_plan(analysis: dict) -> str:
    latest = analysis["latest"]
    lines = [
        f"# Next Week Operating Plan: {latest['week']}",
        "",
        "## Focus",
        "",
    ]
    lines.extend(
        f"{index}. {priority}"
        for index, priority in enumerate(analysis["priorities"], start=1)
    )
    lines.extend(
        [
            "",
            "## Founder Checkpoints",
            "",
            "- Monday: confirm the one growth constraint and one product constraint.",
            "- Wednesday: review pipeline movement, support load, and activation blockers.",
            "- Friday: decide what moves into the next investor update.",
            "",
        ]
    )
    return "\n".join(lines)
