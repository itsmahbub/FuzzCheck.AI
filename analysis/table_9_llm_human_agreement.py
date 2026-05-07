"""
Computes per-metric agreement between:
  (1) the 3 human experts (all three assign the same value), and
  (2) the preliminary LLM labels vs. expert-validated labels
"""
import json
from collections import defaultdict

# ── Load data ─────────────────────────────────────────────────────────────────
with open("results/assessments.json", "r") as f:
    data = json.load(f)

author_files = {
    "E1": "results/assessments_author1.json",
    "E2": "results/assessments_author2.json",
    "E3": "results/assessments_author3.json",
}
authors = {}
for label, path in author_files.items():
    with open(path) as f:
        authors[label] = json.load(f)

metrics = {
    "Failure Severity": "Failure Severity",
    "Targeted Attack Discovery": "Targeted Attack Discovery",
    "Input Plausibility": "Input Plausibility",
    "Failure Reproducibility": "Failure Reproducibility",
    "Failure Diagnostics": "Failure Diagnostics",
    "Attack Transferability": "Attack Transferability"
}

# ── Initialize counters ───────────────────────────────────────────────────────
llm_agreement_counts   = defaultdict(int)   # LLM vs expert
expert_agreement_counts = defaultdict(int)  # all 3 experts agree
total_counts           = defaultdict(int)

# ── LLM vs expert agreement (from assessments.json) ──────────────────────────
for paper in data.values():
    assessments = paper.get("assessments", {})
    for metric in metrics:
        if metric in assessments:
            try:
                manual = assessments[metric]["manual"]["value"]
                llm    = assessments[metric]["arbitrator"]["value"]
            except Exception as e:
                print(paper["key"])
                raise e
            total_counts[metric] += 1
            if manual == llm:
                llm_agreement_counts[metric] += 1

# ── 3-way expert agreement (all three experts assign the same value) ──────────
paper_keys = list(authors["E1"].keys())
for paper_key in paper_keys:
    for metric in metrics:
        values = []
        for label in author_files:
            try:
                v = authors[label][paper_key]["assessments"][metric]["manual"]["value"]
                values.append(v)
            except (KeyError, TypeError):
                values.append(None)
        if all(v is not None for v in values) and len(set(values)) == 1:
            expert_agreement_counts[metric] += 1

# ── Generate LaTeX table rows ─────────────────────────────────────────────────
latex_rows = []
overall_llm_agreement    = 0
overall_expert_agreement = 0
overall_total            = 0

for metric in metrics:
    total                  = total_counts[metric]
    llm_expert_agreement   = llm_agreement_counts[metric]
    expert_agreement       = expert_agreement_counts[metric]
    llm_expert_agreement_rate = round((llm_expert_agreement / total) * 100, 1) if total > 0 else 0.0
    expert_agreement_rate     = round((expert_agreement    / total) * 100, 1) if total > 0 else 0.0

    row = (
        f"{metrics[metric]} & "
        f"{expert_agreement}/{total} ({expert_agreement_rate}\\%) & & "
        f"{llm_expert_agreement}/{total} ({llm_expert_agreement_rate}\\%) \\\\"
    )
    latex_rows.append(row)
    overall_llm_agreement    += llm_expert_agreement
    overall_expert_agreement += expert_agreement
    overall_total            += total

# Add overall row
overall_llm_rate    = round((overall_llm_agreement    / overall_total) * 100, 1) if overall_total > 0 else 0.0
overall_expert_rate = round((overall_expert_agreement / overall_total) * 100, 1) if overall_total > 0 else 0.0
overall_row = (
    f"\\textbf{{Overall}} & "
    f"\\textbf{{{overall_expert_agreement}/{overall_total} ({overall_expert_rate}\\%)}} & & "
    f"\\textbf{{{overall_llm_agreement}/{overall_total} ({overall_llm_rate}\\%)}} \\\\"
)
latex_rows.append("\\hline")
latex_rows.append(overall_row)

# Print LaTeX rows
for row in latex_rows:
    print(row)
