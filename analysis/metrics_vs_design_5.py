import json
from collections import defaultdict

# ---------- CONFIG ----------
input_file = "results/assessments.json"

metrics = [
    "Failure Severity",
    "Targeted Attack Discovery",
    "Input Plausibility",
    "Failure Reproducibility",
    "Failure Diagnostics",
    "Attack Transferability",
]


metric_levels = {
    "Failure Severity": ["High", "Medium", "Low"],
    "Targeted Attack Discovery": ["High", "Medium", "Low"],
    "Input Plausibility": ["High", "Medium", "Low"],
    "Failure Reproducibility": ["High", "Medium", "Low"],
    "Failure Diagnostics": ["High", "Medium", "Low"],
    "Attack Transferability": ["High", "Medium", "Low"]
}

taxonomy_groups = {
    "Access": "access_level",
    "Mutation": "mutation_strategy",
    "Exploration": "exploration_strategy",
    "Oracle": "oracle",
}

# Fixed column order for consistent table layout
GROUP_CATEGORY_ORDER = {
    "Access": ["Whitebox", "Greybox", "Blackbox"],
    "Mutation": ["Feedback-informed", "Rule-based", "Generative Synthesized"],
    "Exploration": ["Coverage-guided", "Prediction-guided", "Oracle-guided", "Data-driven"],
    "Oracle": ["Metamorphic", "Differential", "Property-based"],
}

# ---------- LOAD ----------
with open(input_file, "r") as f:
    data = json.load(f)

# ---------- COUNT ----------
counts = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: defaultdict(int))))

for paper_id, info in data.items():
    taxonomy = info.get("taxonomy", {}) or {}
    assessments = info.get("assessments", {}) or {}

    for metric, levels in metric_levels.items():
        m = assessments.get(metric, {}) or {}
        level = m["manual"]["value"]
  
        for group, key in taxonomy_groups.items():
            cats = taxonomy.get(key, [])
            for cat in cats:
                if cat not in GROUP_CATEGORY_ORDER[group]:
                    raise Exception(f"Unrecognized category {cat}")
                counts[metric][group][cat]["__total__"] += 1

                counts[metric][group][cat][level] += 1

# Ensure all combinations exist for printing
for metric in metric_levels:
    for group, cat_order in GROUP_CATEGORY_ORDER.items():
        for cat in cat_order:
            _ = counts[metric][group][cat]["__total__"]  # initialize empty


# ---------- PRINT (LaTeX) ----------
def pct_cell(numer, denom):
    pct = 0 if denom == 0 else round(100 * numer / denom)
    return f"\\cellcolor{{gray!15}}{pct}" if pct > 50 else f"{pct}"

def print_metrics(metrics):
  
    for metric in metrics:
        levels = metric_levels[metric]
        nrows = len(levels)
        for i, lvl in enumerate(levels):
            mname = metric.replace(" ", "\\\\")  # multiline name
            lead = f"\\multirow{{{len(levels)}}}{{*}}{{\\makecell[l]{{{mname}}}}}" if i == 0 else ""

            
            print(lead + f"& \\{lvl.lower()}", end=" ")

            # Column order: Access → Mutation → Exploration → Oracle
            for group in ["Access", "Mutation", "Exploration", "Oracle"]:
                for cat in GROUP_CATEGORY_ORDER[group]:
                    denom = counts[metric][group][cat]["__total__"]
                    numer = counts[metric][group][cat][lvl]
                    print(f"& {pct_cell(numer, denom)}", end=" ")
            print("\\\\")
        print("\\hline\n")

# ---------- GENERATE FULL TABLE ----------
print_metrics(metrics)
