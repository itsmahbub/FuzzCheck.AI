"""
taxonomy_distribution.py

Counts how many papers fall under each value of each taxonomy dimension,
based on results/assessments.json.

Taxonomy dimensions:
  - oracle              (e.g., Metamorphic, Differential, Property-based)
  - access_level        (e.g., Blackbox, Greybox, Whitebox)
  - mutation_strategy   (e.g., Rule-based, Generative Synthesized, Feedback-informed)
  - exploration_strategy(e.g., Coverage-guided, Prediction-guided, Data-driven)
"""

import json
from pathlib import Path
from collections import defaultdict


# ── load data ─────────────────────────────────────────────────────────────────
with open("results/assessments.json", encoding="utf-8") as f:
    data = json.load(f)

total_papers = len(data)

# ── count papers per taxonomy value ──────────────────────────────────────────
# Structure: {dimension: {value: count}}
counts: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))

for paper_content in data.values():
    taxonomy = paper_content.get("taxonomy", {})
    for dimension, values in taxonomy.items():
        for value in values:
            counts[dimension][value] += 1

# ── pretty print ──────────────────────────────────────────────────────────────
DIMENSION_LABELS = {
    "oracle":               "Oracle Type",
    "access_level":         "Access Level",
    "mutation_strategy":    "Mutation Strategy",
    "exploration_strategy": "Exploration Strategy",
}


print()
print("=" * 62)
print(f"  TAXONOMY DISTRIBUTION  —  {total_papers} papers total")
print("=" * 62)

for dim_key in ["oracle", "access_level", "mutation_strategy", "exploration_strategy"]:
    label = DIMENSION_LABELS.get(dim_key, dim_key)
    dim_counts = counts.get(dim_key, {})

    # sort by count descending
    sorted_values = sorted(dim_counts.items(), key=lambda x: x[1], reverse=True)

    print()
    print(f"  ┌─ {label} {'─' * (55 - len(label))}")
    for value, count in sorted_values:
        pct = count / total_papers * 100
        print(f"  │  {value:<22}  {count:>3} papers  ({pct:4.1f}%)")
    print(f"  └{'─' * 57}")

print()
print("Note: A paper may appear under multiple values within a")
print("      dimension, so column totals can exceed the paper count.")
print()
