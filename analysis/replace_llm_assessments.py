#!/usr/bin/env python3

import argparse
import json
import sys
from copy import deepcopy
from pathlib import Path

DEFAULT_BASE = Path(__file__).parent / "results" / "assessments_mahbub.json"
PROTECTED_PAPER_KEYS = {"key", "name", "year", "citation_count", "conf/journal", "type"}
PROTECTED_ASSESSOR = "manual"


def load_json(path: Path) -> dict:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def save_json(path: Path, data: dict) -> None:
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh, indent=4, ensure_ascii=False)
    print(f"[saved] {path}")


def apply_updates(
    source_data: dict,
    target_data: dict,
):
    """
    Merge source data into target.
    """
    for paper_title, paper_data in source_data.items():
        if paper_title not in target_data:
            print(
                f"[warning] Paper not found in target file, skipping: {paper_title!r}",
                file=sys.stderr,
            )
            continue

        for metric in paper_data["assessments"]:
            target_data[paper_title]["assessments"][metric]["chatgpt"] = paper_data["assessments"][metric]["chatgpt"] 
            target_data[paper_title]["assessments"][metric]["gemini"] = paper_data["assessments"][metric]["gemini"]
            target_data[paper_title]["assessments"][metric]["arbitrator"] = paper_data["assessments"][metric]["arbitrator"] 
    return target_data
       


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Replace chatgpt/gemini/arbitrator assessments in target by source json"
    )
    parser.add_argument(
        "--target",
        type=Path,
        help=f"Path to the target assessments file",
    )
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="Path to the JSON file containing the new assessments to merge in",
    )

    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Parse and validate without writing any files",
    )

    args = parser.parse_args()

    source_data = load_json(args.source)
    target_data = load_json(args.target)


    updated_target_data = apply_updates(
        source_data,
        target_data
    )


    if args.dry_run:
        print("\n[dry-run] No files written.")
        return

    save_json(args.target, updated_target_data)


if __name__ == "__main__":
    main()
