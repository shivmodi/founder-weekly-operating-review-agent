# Founder Weekly Operating Review Agent

## Problem This Solves

Founders lose time turning scattered weekly metrics into a clear operating narrative. The problem is not knowing the numbers; it is deciding what changed, what is risky, what needs action, and what can be safely shared with investors.

## How It Helps

- Converts a weekly metrics CSV and company context into a CEO-ready operating review.
- Produces risks, priorities, team asks, an investor-safe update, and a next-week execution plan.
- Gives founders and founder's office operators a forkable cadence for weekly business reviews before they have a full BizOps, RevOps, or FP&A function.

## When To Fork This

- Fork this if your weekly review is still built manually from spreadsheets, Slack notes, and founder memory.
- Fork it when leadership needs one operating packet that connects growth, churn, activation, pipeline, runway, support load, and product issues.
- Replace the sample metrics, thresholds, and output format with your company's operating cadence.

## What It Produces

```text
weekly_operating_review.md   CEO-ready weekly review
investor_safe_update.md      External-safe investor narrative
team_asks.md                 Clear asks by function
next_week_plan.md            Focus areas and execution plan
analysis.json                Structured metric deltas, risks, and priorities
```

## Quickstart

```bash
git clone https://github.com/shubham1502-hue/founder-weekly-operating-review-agent.git
cd founder-weekly-operating-review-agent

python3 -m founder_weekly_review \
  --metrics examples/weekly_metrics.csv \
  --context examples/company_context.md \
  --out outputs/demo \
  --config examples/thresholds.json
```

Then open:

- `outputs/demo/weekly_operating_review.md`
- `outputs/demo/investor_safe_update.md`
- `outputs/demo/team_asks.md`
- `outputs/demo/next_week_plan.md`
- `outputs/demo/analysis.json`

## Custom Risk Thresholds

You can override the default risk thresholds by passing a JSON (or YAML) config file via the `--config` argument.

Example JSON (`examples/thresholds.json`):

````json
{
  "runway_months": 10,
  "churn_rate": 0.05,
  "activation_drop": 0.01,
  "support_growth": 0.05,
  "nps": 25
}

## Demo Output Preview

See [docs/sample_weekly_operating_review.md](docs/sample_weekly_operating_review.md) for a generated example.

## Project Structure

```text
founder-weekly-operating-review-agent/
├── examples/
│   ├── company_context.md
│   └── weekly_metrics.csv
├── src/founder_weekly_review/
│   ├── analysis.py
│   ├── cli.py
│   ├── metrics.py
│   └── reporting.py
├── tests/
│   └── test_analysis.py
└── README.md
````

## Metrics Expected

The sample CSV includes:

- MRR, new MRR, expansion MRR, churn MRR
- Active customers, new customers, churned customers
- Activation rate
- Pipeline value
- Cash balance, burn, runway
- Open support tickets
- NPS
- Open product issues

## Why This Matters

This repo is built for the founder's office job to be done: absorb messy operating signal, identify what deserves leadership attention, and convert it into a weekly cadence that makes decisions faster.

## License

MIT
