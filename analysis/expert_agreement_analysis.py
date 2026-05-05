#!/usr/bin/env python3
"""
Compare manual assessments across two or more assessments.json files.
Usage: python expert_agreement_analysis.py <file1.json> <file2.json> [file3.json ...]
"""

import json
import sys
from itertools import combinations

if len(sys.argv) < 3:
    print("Usage: python expert_agreement_analysis.py <file1.json> <file2.json> [file3.json ...]")
    sys.exit(1)

filenames = sys.argv[1:]

# Load all files
datasets = {}
for fname in filenames:
    with open(fname) as f:
        datasets[fname] = json.load(f)

papers = datasets[filenames[0]].keys()

# ── Overall disagreements (any two files differ) ─────────────────────────────
diffs = []
total = 0

for paper in papers:
    for metric, assessment in datasets[filenames[0]][paper]["assessments"].items():
        entries = [
            {"file": fname,
             "value": datasets[fname][paper]["assessments"][metric]["manual"]["value"],
             "why":   datasets[fname][paper]["assessments"][metric]["manual"]["why"]}
            for fname in filenames
        ]
        total += 1
        if len(set(e["value"] for e in entries)) > 1:
            diffs.append({
                "paper": datasets[filenames[0]][paper].get("key", paper),
                "metric": metric,
                "entries": entries,
            })

# ── Print overall disagreements ───────────────────────────────────────────────
if not diffs:
    print("No differences found in manual assessments.")
else:
    print(f"Found {len(diffs)} disagreement(s) (out of {total} metric×paper pairs):\n")
    for d in diffs:
        print(f"Paper  : {d['paper']}")
        print(f"Metric : {d['metric']}")
        for e in d["entries"]:
            print(f"  {e['file']}: {e['value']}")
            print(f"    Why: {e['why']}")
        print()

# ── Overall agreement rate (all files agree) ──────────────────────────────────
agreed_all = total - len(diffs)
rate_all = (agreed_all / total * 100) if total > 0 else 0
print(f"Overall agreement (all {len(filenames)} files): {agreed_all}/{total} ({rate_all:.1f}%)")

# ── Pairwise agreement rates ──────────────────────────────────────────────────
if len(filenames) > 2:
    print()
    for f1, f2 in combinations(filenames, 2):
        pair_total = 0
        pair_agreed = 0
        for paper in papers:
            for metric in datasets[f1][paper]["assessments"]:
                v1 = datasets[f1][paper]["assessments"][metric]["manual"]["value"]
                v2 = datasets[f2][paper]["assessments"][metric]["manual"]["value"]
                pair_total += 1
                if v1 == v2:
                    pair_agreed += 1
        pair_rate = (pair_agreed / pair_total * 100) if pair_total > 0 else 0
        print(f"Pairwise {f1} vs {f2}: {pair_agreed}/{pair_total} ({pair_rate:.1f}%)")
