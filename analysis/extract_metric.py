#!/usr/bin/env python3
"""
extract_metric.py

Produces a filtered assessments JSON containing only a specific metric,
retaining only the 'manual' and 'arbitrator' evaluator entries (chatgpt and
gemini are dropped).

Usage:
    python3 analysis/extract_metric.py "<Metric Name>"

Example:
    python3 analysis/extract_metric.py "Failure Severity"

Output:
    results/assessments_<metric_slug>.json

The output file has the same top-level structure as assessments.json but each
paper's 'assessments' dict contains only the requested metric, and within that
metric only the 'manual' and 'arbitrator' keys are kept.
"""

import json
import sys
import os
import re




KEEP_EVALUATORS = {"manual", "arbitrator"}


def slugify(name: str) -> str:
    """Convert a metric name to a safe filename component."""
    slug = name.lower().strip()
    slug = re.sub(r"[^a-z0-9]+", "_", slug)
    slug = slug.strip("_")
    return slug


def extract_metric(metric_name: str) -> None:
    # Load source data
    with open("results/assessments.json", "r", encoding="utf-8") as f:
        data = json.load(f)

    # Collect all available metric names for validation / error messaging
    available_metrics: set[str] = set()
    for paper_data in data.values():
        available_metrics.update(paper_data.get("assessments", {}).keys())

    if metric_name not in available_metrics:
        print(f"ERROR: Metric '{metric_name}' not found in assessments.")
        print("Available metrics:")
        for m in sorted(available_metrics):
            print(f"  - {m}")
        sys.exit(1)

    # Build filtered output
    output: dict = {}
    papers_missing_metric = []

    for paper_key, paper_data in data.items():
        assessments = paper_data.get("assessments", {})

        if metric_name not in assessments:
            papers_missing_metric.append(paper_key)
            continue

        metric_entry = assessments[metric_name]

        # Keep only manual and arbitrator evaluators
        filtered_evaluators = {
            k: v for k, v in metric_entry.items() if k in KEEP_EVALUATORS
        }

        # Copy paper metadata; replace assessments with the single filtered metric
        filtered_paper = {k: v for k, v in paper_data.items() if k != "assessments"}
        filtered_paper["assessments"] = {metric_name: filtered_evaluators}

        output[paper_key] = filtered_paper

    # Write output
    slug = slugify(metric_name)
    output_path = os.path.join("results", f"assessments_{slug}.json")
    with open(output_path, "w", encoding="utf-8") as f:
        json.dump(output, f, indent=2, ensure_ascii=False)

    # Report
    print(f"Metric   : {metric_name}")
    print(f"Papers   : {len(output)} included")
    if papers_missing_metric:
        print(f"Skipped  : {len(papers_missing_metric)} paper(s) had no entry for this metric:")
        for p in papers_missing_metric:
            print(f"  - {p}")
    print(f"Output   : {os.path.abspath(output_path)}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python3 analysis/extract_metric.py \"<Metric Name>\"")
        print()
        print("Available metrics (reading from assessments.json):")
        try:
            with open("results/assessments.json", "r", encoding="utf-8") as f:
                data = json.load(f)
            metrics: set[str] = set()
            for paper_data in data.values():
                metrics.update(paper_data.get("assessments", {}).keys())
            for m in sorted(metrics):
                print(f"  - {m}")
        except FileNotFoundError:
            print("  (could not open results/assessments.json)")
        sys.exit(1)

    extract_metric(sys.argv[1])
