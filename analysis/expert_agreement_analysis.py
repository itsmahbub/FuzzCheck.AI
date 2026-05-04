#!/usr/bin/env python3
"""
Compare manual assessments between two assessments.json files.
Usage: python compare_manual.py <file1.json> <file2.json>
"""

import json
import sys

file1, file2 = sys.argv[1], sys.argv[2]

with open(file1) as f:
    data1 = json.load(f)
with open(file2) as f:
    data2 = json.load(f)

diffs = []
total = 0

for paper in data1:
    if paper not in data2:
        continue
    for metric, assessment in data1[paper]["assessments"].items():
        v1 = assessment["manual"]["value"]
        v2 = data2[paper]["assessments"][criterion]["manual"]["value"]
        total += 1
        if v1 != v2:
            diffs.append({
                "paper": data1[paper].get("key", paper),
                "metric": metric,
                file1: v1,
                file2: v2,
            })


if not diffs:
    print("No differences found in manual assessments.")
else:
    print(f"Found {len(diffs)} difference(s):\n")
    for d in diffs:
        print(f"Paper    : {d['paper']}")
        print(f"Metric: {d['metric']}")
        print(f"  {file1}: {d[file1]}")
        print(f"  {file2}: {d[file2]}")
        print()

agreed = total - len(diffs)
rate = (agreed / total * 100) if total > 0 else 0
print(f"Agreement rate: {agreed}/{total} ({rate:.1f}%)\n")
