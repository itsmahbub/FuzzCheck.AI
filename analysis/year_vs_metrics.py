import json
from collections import defaultdict

# ---------- CONFIG ----------
input_file = "results/assessments.json"

metric_levels = {
    "Failure Severity": ["High", "Medium", "Low"],
    "Targeted Attack Discovery": ["High", "Medium", "Low"],
    "Root-Cause Analysis": ["High", "Medium", "Low"],
    "Input Plausibility": ["High", "Medium", "Low"],
    "Failure Reproducibility": ["High", "Medium", "Low"],
    "Attack Transferability": ["High", "Low"],  # only two levels
}

# ---------- LOAD JSON ----------
with open(input_file, "r") as f:
    data = json.load(f)

# ---------- COUNT BY YEAR ----------
summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
paper_sets = defaultdict(set)

for paper, info in data.items():
    year = str(info.get("year", "")).strip()
    if not year:
        continue
    paper_sets[year].add(paper)
    assessments = info.get("assessments", {})

    for metric, levels in metric_levels.items():
        metric_data = assessments.get(metric, {})
        val = (metric_data.get("manual", {}) or {}).get("value", "").strip()
        if not val:
            val = (metric_data.get("llm", {}) or {}).get("value", "").strip()
        if not val:
            continue
        val = val.capitalize()
        if val not in levels:
            continue
        summary[year][metric][val] += 1

# ---------- PRINT LATEX ROWS ----------
for year in sorted(summary.keys(), reverse=True):
    row = [year]

    # paper count
    count = len(paper_sets[year])
    row.append(f"\\textbf{{{count}}}")

    # metric percentages
    for metric, levels in metric_levels.items():
        total = sum(summary[year][metric].values())
        for lvl in levels:
            pct = 0 if total == 0 else round((summary[year][metric].get(lvl, 0) / total) * 100)
            if pct > 50:
                formated_pct = f"\\cellcolor{{gray!15}}{pct}"
            else:
                formated_pct = f"{pct}"
            row.append(formated_pct)

    print(" & ".join(row) + " \\\\")
print("\\hline \\hline")