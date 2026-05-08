import sys
from pathlib import Path
import tempfile
import unittest

# Adjust sys.path so test can import the package
ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "src"))

from founder_weekly_review.analysis import analyze
from founder_weekly_review.metrics import load_metrics
from founder_weekly_review.reporting import write_outputs


class WeeklyReviewTests(unittest.TestCase):
    def test_load_metrics_and_build_analysis(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics, context="Test context")

        self.assertEqual(result["latest"]["week"], "2026-W06")
        self.assertGreater(result["deltas"]["mrr_growth"], 0)
        self.assertGreaterEqual(len(result["risks"]), 1)
        self.assertGreaterEqual(len(result["priorities"]), 1)

    def test_writes_expected_outputs(self):
        metrics = load_metrics(ROOT / "examples" / "weekly_metrics.csv")
        result = analyze(metrics)

        with tempfile.TemporaryDirectory() as tmp:
            out_dir = Path(tmp)
            write_outputs(result, out_dir)
            self.assertTrue((out_dir / "weekly_operating_review.md").exists())
            self.assertTrue((out_dir / "investor_safe_update.md").exists())
            self.assertTrue((out_dir / "team_asks.md").exists())
            self.assertTrue((out_dir / "next_week_plan.md").exists())
            self.assertTrue((out_dir / "analysis.json").exists())

    # Custom threshold test: ensures JSON config affects risks
    # Threshold values are read dynamically from examples/thresholds.json
    # This verifies that risks are correctly triggered or suppressed
    def test_custom_thresholds_loaded_from_json(self):
        # Load metrics
        metrics = load_metrics(ROOT / "examples/weekly_metrics.csv")

        # Load thresholds from JSON (like CLI)
        threshold_file = ROOT / "examples/thresholds.json"
        import json

        with threshold_file.open("r", encoding="utf-8") as f:
            thresholds = json.load(f)

        # Run analysis with thresholds
        result = analyze(metrics, thresholds=thresholds)

        # Extract risk areas
        risk_areas = [r["area"] for r in result["risks"]]

        # Check each metric threshold
        if thresholds["runway_months"] > metrics[-1].runway_months:
            self.assertIn("cash", risk_areas)
        else:
            self.assertNotIn("cash", risk_areas)

        if thresholds["churn_rate"] < metrics[-1].churn_mrr / max(metrics[-2].mrr, 1):
            self.assertIn("retention", risk_areas)
        else:
            self.assertNotIn("retention", risk_areas)

        if (
            thresholds["activation_drop"]
            < metrics[-1].activation_rate - metrics[-2].activation_rate
        ):
            self.assertIn("activation", risk_areas)
        else:
            self.assertNotIn("activation", risk_areas)

        if thresholds["support_growth"] < (
            metrics[-1].support_tickets_open - metrics[-2].support_tickets_open
        ) / max(metrics[-2].support_tickets_open, 1):
            self.assertIn("support", risk_areas)
        else:
            self.assertNotIn("support", risk_areas)

        if thresholds["nps"] > metrics[-1].nps:
            self.assertIn("customer sentiment", risk_areas)
        else:
            self.assertNotIn("customer sentiment", risk_areas)


if __name__ == "__main__":
    unittest.main()
