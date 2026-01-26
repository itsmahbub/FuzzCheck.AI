import json
from collections import defaultdict

# ---------- CONFIG ----------
input_file = "results/assessments.json"

metric_levels = {
    "Failure Severity": ["High", "Medium", "Low"],
    "Targeted Attack Discovery": ["High", "Medium", "Low"],
    "Root-Cause Analysis": ["High", "Medium", "Low"],
    "Input Plausibility": ["High", "Medium", "Low"],
    "Failure Reproducibility": ["High", "Medium", "Low"],   # formerly Fault Stability
    "Attack Transferability": ["High", "Medium", "Low"],
}

metric_groups = {
    "Diagnostic Capability": [
        "Failure Severity",
        "Targeted Attack Discovery",
        "Root-Cause Analysis",
    ],
    "Functional Integrity": [
        "Input Plausibility",
        "Failure Reproducibility",
    ],
    "Generality": [
        "Attack Transferability",
    ],
}

# ---------- LOAD JSON ----------
with open(input_file, "r") as f:
    data = json.load(f)

# ---------- BUILD SUMMARY ----------
summary = defaultdict(lambda: defaultdict(lambda: defaultdict(int)))
years = set()

for paper, info in data.items():
    year = str(info.get("year", "")).strip()
    if not year:
        continue
    years.add(year)
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

# ---------- PREPARE YEARS ----------
years = sorted(years)  # oldest → newest
n_years = len(years)

# ---------- GENERATE LATEX ----------
def pct(year, metric, lvl):
    s = summary[year][metric]
    total = sum(s.values())
    if total == 0:
        return 0
    return round((s.get(lvl, 0) / total) * 100)


for group_name, metrics in metric_groups.items():
    # print("\\hline")
    # print("\\hline")
    # print(f"\\multicolumn{{{n_years + 2}}}{{|c|}}{{\\textbf{{{group_name}}}}}\\\\")
    # print("\\hline")
    # print("\\hline")

    print("\\hline\n\\hline")
    print(f"\\multicolumn{{{n_years + 2}}}{{|c|}}{{\\cellcolor{{gray!10}}\\textbf{{{group_name}}}}}\\\\")
    print("\\arrayrulecolor{black!50}\n\\hline\n\\hline")

    for metric in metrics:
        levels = metric_levels[metric]
        mname = metric.replace(" ", "\\\\")  # multiline name
        print(f"\\multirow{{{len(levels)}}}{{*}}{{\\makecell[l]{{{mname}}}}}", end="")

        for i, lvl in enumerate(levels):
            label = "\\high" if lvl == "High" else "\\medium" if lvl == "Medium" else "\\low"
            if i > 0:
                print(f"& {label}", end="")
            else:
                print(f" & {label}", end="")

            for year in years:
                value = pct(year, metric, lvl)
                cell = f"\\cellcolor{{gray!15}}{value}" if value > 50 else str(value)
                print(f" & {cell}", end="")
            print(" \\\\")

        print("\\hline")

