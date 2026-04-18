#!/usr/bin/env python3
import argparse
import json
from pathlib import Path


def blank_manual_entries(value):
    if isinstance(value, dict):
        cleaned = {}
        for key, child in value.items():
            if key == "manual" and isinstance(child, dict):
                cleaned[key] = {
                    nested_key: "" if isinstance(nested_value, str) else nested_value
                    for nested_key, nested_value in child.items()
                }
            else:
                cleaned[key] = blank_manual_entries(child)
        return cleaned
    if isinstance(value, list):
        return [blank_manual_entries(item) for item in value]
    return value


def main():
    parser = argparse.ArgumentParser(
        description="Blank all values inside 'manual' entries in an assessments JSON file."
    )
    parser.add_argument(
        "input",
        nargs="?",
        default="results/assessments.json",
        help="Path to the input JSON file. Defaults to results/assessments_sonjoy.json.",
    )
    parser.add_argument(
        "-o",
        "--output",
        default="results/assessments_blank.json",
        help="Path to write the cleaned JSON.",
    )
    args = parser.parse_args()

    input_path = Path(args.input)
    output_path = Path(args.output) if args.output else input_path

    with input_path.open("r", encoding="utf-8") as f:
        data = json.load(f)

    cleaned = blank_manual_entries(data)

    with output_path.open("w", encoding="utf-8") as f:
        json.dump(cleaned, f, indent=4, ensure_ascii=False)
        f.write("\n")


if __name__ == "__main__":
    main()
