#!/usr/bin/env python3


import json
import sys
from collections import Counter

assessments_file = sys.argv[1] if len(sys.argv) > 1 else "results/assessments.json"
venues_file      = sys.argv[2] if len(sys.argv) > 2 else "venues.json"

with open(assessments_file) as f:
    data = json.load(f)
with open(venues_file) as f:
    venues = json.load(f)

counts = Counter(entry.get("conf/journal", "Unknown") for entry in data.values())

conferences = []
journals    = []

for venue, count in sorted(counts.items(), key=lambda x: -x[1]):
    info  = venues.get(venue, {})
    # name  = info.get("name", venue)   # full name, fall back to key
    name = venue
    rank  = info.get("rank", "N/A")
    row   = (name, rank, count)
    if info.get("type") == "conference":
        conferences.append(row)
    else:
        journals.append(row)

def print_row(name, rank, count):
    print(f"{name} & {rank} & {count} \\\\")

# Header
print(r"\textbf{Venue} & \textbf{Rank} & \textbf{\#} \\ \midrule")

# Conferences
print(r"\multicolumn{3}{l}{\textbf{Conferences}} \\ \midrule")
for row in conferences:
    print_row(*row)

# Journals / arXiv
print(r"\midrule")
print(r"\multicolumn{3}{l}{\textbf{Journals / arXiv}} \\ \midrule")
for row in journals:
    print_row(*row)
