from __future__ import annotations

import argparse
from pathlib import Path

from .analysis import analyze
from .metrics import load_metrics
from .reporting import write_outputs


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Generate a founder weekly operating review."
    )
    parser.add_argument(
        "--metrics", required=True, type=Path, help="Weekly metrics CSV."
    )
    parser.add_argument("--context", type=Path, help="Company context Markdown file.")
    parser.add_argument(
        "--out", type=Path, default=Path("outputs/demo"), help="Output directory."
    )
    parser.add_argument(
        "--config", type=Path, help="JSON or YAML file with risk thresholds"
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    context = args.context.read_text(encoding="utf-8") if args.context else ""
    metrics = load_metrics(args.metrics)
    # Default thresholds — used if user does not provide --config
    thresholds = {
        "runway_months": 6,
        "churn_rate": 0.06,
        "activation_drop": 0.03,
        "support_growth": 0.15,
        "nps": 30,
    }
    # If user passes JSON/YAML config, override defaults
    if args.config:
        if not args.config.exists():
            raise FileNotFoundError(f"Config file not found: {args.config}")
        import json

        # Load user thresholds from config file
        with args.config.open("r", encoding="utf-8") as f:
            user_thresholds = json.load(f)
            thresholds.update(user_thresholds)
    print(f"DEBUG: thresholds loaded from JSON: {thresholds}", flush=True)

    result = analyze(metrics, context=context, thresholds=thresholds)
    write_outputs(result, args.out)
    print(f"Generated weekly operating review in {args.out}")
    return 0


# Temporary direct-run support for debugging
# Normally we run CLI via `python -m src.founder_weekly_review.cli`
if __name__ == "__main__":
    main()
