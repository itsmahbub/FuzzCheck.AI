import argparse
import json
from pathlib import Path


TARGET_MODELS = ("chatgpt", "gemini", "arbitrator")


def reset_llm_assessments(data):
    reset_count = 0

    for paper in data.values():
        assessments = paper.get("assessments", {})
        for metric in assessments.values():
            for model_name in TARGET_MODELS:
                if model_name in metric:
                    del metric[model_name]
                    reset_count += 1

    return reset_count


def main():
    parser = argparse.ArgumentParser(
        description=(
            "Reset chatgpt, gemini, and arbitrator assessment entries for all "
            "metrics across all papers in an assessments JSON file."
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

    reset_count = reset_llm_assessments(data)

    with json_path.open("w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)
        f.write("\n")

    print(f"Reset {reset_count} model assessment entries in {json_path}")


if __name__ == "__main__":
    main()
