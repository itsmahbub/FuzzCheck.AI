"""
Computes per-metric inter-expert agreement among 3 human experts.
Expert labels come from the "manual" field in each assessments_authorN.json file.

Agreement is measured as:
  - Pairwise: % of papers where two experts assign the same value
  - Full (3-way): % of papers where all three experts agree
"""
import json
from collections import defaultdict

AUTHOR_FILES = {
    "E1": "results/assessments_author1.json",
    "E2": "results/assessments_author2.json",
    "E3": "results/assessments_author3.json",
}

METRICS = [
    "Failure Severity",
    "Targeted Attack Discovery",
    "Input Plausibility",
    "Failure Reproducibility",
    "Failure Diagnostics",
    "Attack Transferability",
]

PAIRS = [("E1", "E2"), ("E1", "E3"), ("E2", "E3")]

# ── Load data ─────────────────────────────────────────────────────────────────
authors = {}
for label, path in AUTHOR_FILES.items():
    with open(path) as f:
        authors[label] = json.load(f)

# All paper keys must be identical across files
paper_keys = list(authors["E1"].keys())
assert set(paper_keys) == set(authors["E2"].keys()) == set(authors["E3"].keys()), \
    "Paper keys differ across author files!"

# ── Count agreements ──────────────────────────────────────────────────────────
pair_agree  = {p: defaultdict(int) for p in PAIRS}
pair_total  = {p: defaultdict(int) for p in PAIRS}
full_agree  = defaultdict(int)   # all 3 match
full_total  = defaultdict(int)   # papers where all 3 have a value

for paper_key in paper_keys:
    for metric in METRICS:
        values = {}
        for label in AUTHOR_FILES:
            try:
                v = (authors[label][paper_key]
                     ["assessments"][metric]["manual"]["value"])
                values[label] = v
            except (KeyError, TypeError):
                values[label] = None  # missing assessment

        # Pairwise
        for (a, b) in PAIRS:
            va, vb = values[a], values[b]
            if va is not None and vb is not None:
                pair_total[(a, b)][metric] += 1
                if va == vb:
                    pair_agree[(a, b)][metric] += 1

        # Full 3-way
        if all(v is not None for v in values.values()):
            full_total[metric] += 1
            if len(set(values.values())) == 1:
                full_agree[metric] += 1

# ── Helper ────────────────────────────────────────────────────────────────────
def pct(num, den):
    return round(num / den * 100, 1) if den else 0.0

def fmt(num, den):
    return f"{num}/{den} ({pct(num, den)}\\%)"

# ── Build LaTeX table ─────────────────────────────────────────────────────────
header = (
    "\\begin{tabular}{lcccc}\n"
    "\\hline\n"
    "\\textbf{Metric} & "
    "\\textbf{E1 vs E2} & "
    "\\textbf{E1 vs E3} & "
    "\\textbf{E2 vs E3} & "
    "\\textbf{All 3 Agree} \\\\\n"
    "\\hline"
)

rows = [header]

p_overall_agree = {p: 0 for p in PAIRS}
p_overall_total = {p: 0 for p in PAIRS}
f_overall_agree = 0
f_overall_total = 0

for metric in METRICS:
    cols = []
    for pair in PAIRS:
        a, t = pair_agree[pair][metric], pair_total[pair][metric]
        p_overall_agree[pair] += a
        p_overall_total[pair] += t
        cols.append(fmt(a, t))
    fa, ft = full_agree[metric], full_total[metric]
    f_overall_agree += fa
    f_overall_total += ft
    cols.append(fmt(fa, ft))
    rows.append(f"{metric} & " + " & ".join(cols) + " \\\\")

# Overall row
rows.append("\\hline")
overall_cols = []
for pair in PAIRS:
    overall_cols.append(
        f"\\textbf{{{fmt(p_overall_agree[pair], p_overall_total[pair])}}}"
    )
overall_cols.append(
    f"\\textbf{{{fmt(f_overall_agree, f_overall_total)}}}"
)
rows.append("\\textbf{Overall} & " + " & ".join(overall_cols) + " \\\\")
rows.append("\\hline\n\\end{tabular}")

latex = "\n".join(rows)
print(latex)

# ── Also print a plain-text summary ──────────────────────────────────────────
print("\n\n=== Plain-text Summary ===")
header_plain = f"{'Metric':<30} {'E1 vs E2':>18} {'E1 vs E3':>18} {'E2 vs E3':>18} {'All 3':>18}"
print(header_plain)
print("-" * len(header_plain))

for metric in METRICS:
    parts = []
    for pair in PAIRS:
        a, t = pair_agree[pair][metric], pair_total[pair][metric]
        parts.append(f"{a}/{t} ({pct(a,t)}%)")
    fa, ft = full_agree[metric], full_total[metric]
    parts.append(f"{fa}/{ft} ({pct(fa,ft)}%)")
    print(f"{metric:<30} {parts[0]:>18} {parts[1]:>18} {parts[2]:>18} {parts[3]:>18}")

print("-" * len(header_plain))
overall_parts = []
for pair in PAIRS:
    a, t = p_overall_agree[pair], p_overall_total[pair]
    overall_parts.append(f"{a}/{t} ({pct(a,t)}%)")
fa, ft = f_overall_agree, f_overall_total
overall_parts.append(f"{fa}/{ft} ({pct(fa,ft)}%)")
print(f"{'Overall':<30} {overall_parts[0]:>18} {overall_parts[1]:>18} {overall_parts[2]:>18} {overall_parts[3]:>18}")
