import argparse
import json
from pathlib import Path


TARGET_MODELS = ("chatgpt", "gemini", "arbitrator")
RESET_METRICS = None
# Example:
RESET_METRICS = {
    "Failure Diagnostics"
}


def reset_llm_assessments(data, selected_metrics=None):
    reset_count = 0

    for paper in data.values():
        assessments = paper.get("assessments", {})
        for metric_name, metric in assessments.items():
            if selected_metrics is not None and metric_name not in selected_metrics:
                continue
            for model_name in TARGET_MODELS:
                if model_name in metric:
                    del metric[model_name]
                    reset_count += 1

    return reset_count


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Reset chatgpt, gemini, and arbitrator assessment entries for all "
            "or selected metrics across all papers in an assessments JSON file. "
            "Set RESET_METRICS at the top of this script to limit which metrics "
            "are reset."
        )
    )
    parser.add_argument(
        "json_path",
        nargs="?",
        default="results/assessments.json",
        help="Path to the assessments JSON file (default: results/assessments.json)",
    )
    args = parser.parse_args()

    json_path = Path(args.json_path)
    with json_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    reset_count = reset_llm_assessments(data, selected_metrics=RESET_METRICS)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")

    if RESET_METRICS is None:
        scope = "all metrics"
    else:
        scope = f"{len(RESET_METRICS)} selected metrics"
    print(f"Reset {reset_count} model assessment entries in {json_path} ({scope})")


if __name__ == "__main__":
    main()
