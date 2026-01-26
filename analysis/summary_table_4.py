import json
from collections import defaultdict

# === CONFIG ===
input_file = "results/assessments.json"   # path to your JSON file
metrics = [
     "Failure Severity",
    "Targeted Attack Discovery",
    "Input Plausibility",
    "Failure Reproducibility",
    "Root-Cause Analysis",
    "Attack Transferability"
]

# LaTeX symbols for High, Medium, Low
level_symbols = {
    "High": r"\high",      
    "Medium": r"\medium",
    "Low": r"\low"     
}

# === LOAD DATA ===
with open(input_file, "r") as f:
    data = json.load(f)

# === COUNT LEVELS ===
counts = {m: defaultdict(int) for m in metrics}
total_papers = len(data)

for paper_name, paper_data in data.items():
    assessments = paper_data.get("assessments", {})
    for metric in metrics:
        manual_entry = assessments.get(metric, {}).get("manual", {})
        value = manual_entry.get("value", "").strip()
        if value in ["High", "Medium", "Low"]:
            counts[metric][value] += 1


# === BUILD LATEX ROWS ===
rows = []

for level in ["High", "Medium", "Low"]:
    row = [f"{level} ({level_symbols[level]})"]
    for metric in metrics:
        count = counts[metric][level]
        pct = round(100 * counts[metric][level] / total_papers, 1)
        row.append(f"{pct:.0f}\\%")
    rows.append(" & ".join(row) + r" \\")

for row in rows:
    print(row)
