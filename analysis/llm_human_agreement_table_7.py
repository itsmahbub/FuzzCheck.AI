"""
Computes per-metric agreement between preliminary LLM labels and expert-validated labels
"""
import json
from collections import defaultdict

# Load the JSON data
with open("results/assessments.json", "r") as f:
    data = json.load(f)


metrics = {
    "Failure Severity": "Failure Severity",
    "Targeted Attack Discovery": "Targeted Attack Discovery",
    "Input Plausibility": "Input Plausibility",
    "Failure Reproducibility": "Failure Reproducibility",
    "Failure Diagnostics": "Failure Diagnostics",
    "Attack Transferability": "Attack Transferability"
}
# Initialize counters
agreement_counts = defaultdict(int)
total_counts = defaultdict(int)

# Count agreements between manual and LLM assessments
for paper in data.values():
    assessments = paper.get("assessments", {})
    for metric in metrics:
        if metric in assessments:
            manual = assessments[metric]["manual"]["value"]
            llm = assessments[metric]["arbitrator"]["value"]
            total_counts[metric] += 1
            if manual == llm:
                agreement_counts[metric] += 1

# Generate LaTeX table rows
latex_rows = []
overall_agreement = 0
overall_total = 0

for metric in metrics:
    total = total_counts[metric]
    agreement = agreement_counts[metric]
    rate = round((agreement / total) * 100, 1) if total > 0 else 0.0
    row = f"{metrics[metric]} & {agreement}/{total} ({rate}\\%) \\\\"
    latex_rows.append(row)
    overall_agreement += agreement
    overall_total += total

# Add overall row
overall_rate = round((overall_agreement / overall_total) * 100, 1) if overall_total > 0 else 0.0
overall_row = f"\\textbf{{Overall}} & \\textbf{{{overall_agreement}/{overall_total} ({overall_rate}\\%)}} \\\\"
latex_rows.append("\\hline")
latex_rows.append(overall_row)

# Print LaTeX rows
for row in latex_rows:
    print(row)
