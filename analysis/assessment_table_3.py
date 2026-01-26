import json
from itertools import groupby

# Load the JSON file
with open("results/assessments.json", "r") as f:
    data = json.load(f)

# Assessment metrics to include in LaTeX table
assessment_fields = [
    "Failure Severity",
    "Targeted Attack Discovery",
    "Input Plausibility",
    "Failure Reproducibility",
    "Root-Cause Analysis",
    "Attack Transferability",
]

# Mapping of metric values to LaTeX image commands
latex_icon_map = {
    "High": r"\high",
    "Medium": r"\medium",
    "Low": r"\low",
}

# Mapping of taxonomy labels to short forms
taxonomy_label_map = {
    "Metamorphic": "M",
    "Differential": "Df",
    "Property-based": "Pr",
    "Feedback-informed": "F",
    "Rule-based": "R",
    "Generative Synthesized": "G",
    "Coverage-guided": "C",
    "Prediction-guided": "P",
    "Oracle-guided": "O",
    "Data-driven": "D",
}

def format_value(value):
    if isinstance(value, list):
        mapped_values = [latex_icon_map.get(v, v) for v in value]
        return ", ".join(mapped_values)
    if value is None or value == "":
        return "-"
    return latex_icon_map.get(value, str(value))

def map_taxonomy_value(value):
    if isinstance(value, list):
        mapped = [taxonomy_label_map.get(v, v) for v in value]
        return ", ".join(mapped)
    return taxonomy_label_map.get(value, str(value))

def build_row(paper):
    paper_info = paper["name"] + " \\cite{" + paper["key"] + "}"
    year = paper["year"]

    row = [paper_info, year]
    # Add taxonomy (M, E, O)
    mutation = ", ".join(map_taxonomy_value(x) for x in paper["taxonomy"]["mutation_strategy"])
    exploration = ", ".join(map_taxonomy_value(x) for x in paper["taxonomy"]["exploration_strategy"])
    oracle = ", ".join(map_taxonomy_value(x) for x in paper["taxonomy"]["oracle"])

    row.extend([mutation, exploration, oracle])

    # Add assessment metrics
    for field in assessment_fields:
        try:
            metric = paper["assessments"][field]["manual"]["value"]
            if not metric:
                metric = paper["assessments"][field]["arbitrator"]["value"]
            row.append(format_value(metric))
        except Exception as e:
            print("Error processing:", paper_info, field)
            raise e

    
    row.append(paper["taxonomy"]["access_level"][0])  # Keep access level for sorting only

    return row

records = []
for _, paper in data.items():
    year = int(paper["year"])
    citation_count = int(paper["citation_count"])
    row = build_row(paper)
    # Append sort keys for grouping and sorting
    row.extend([-year, -citation_count])
    records.append(row)

# Sort by access level, then year descending, then citation count descending
records.sort(key=lambda r: (r[-3], r[-2], r[-1]))

def emit_table_rows(records):
    grouped = groupby(records, key=lambda r: r[-3])  # group by access level
    for level, group in grouped:
        group = list(group)
        n = len(group)
        print(f"% ===== {level.upper()} FUZZERS =====")
        print("\\hline")
        print(f"\\multicolumn{{11}}{{|c|}}{{\\cellcolor{{gray!10}} \\textbf{{{level}}}}} \\\\")
        print("\\arrayrulecolor{black!50}")
        print("\\hline")
        print("\\hline")
        for row in group:
            row_out = row[:-3]  # drop sort keys and access level
            print(" & ".join(row_out) + r" \\")
            print(r"\hline")  # adjust depending on column count

emit_table_rows(records)
