import json

# Path to your JSON file
with open("results/assessments.json", "r") as f:
    data = json.load(f)

# Metrics in your desired order
assessment_fields = [
     "Failure Severity",
    "Targeted Attack Discovery",
    "Root-Cause Analysis",
    "Input Plausibility",
    "Failure Reproducibility",
    "Attack Transferability"
]

# Value to LaTeX icon mapping
latex_icon_map = {
    "High": r"\high",
    "Medium": r"\medium",
    "Low": r"\low"
}

def format_value(val):
    return latex_icon_map.get(val, val)

def gray_cell(val):
    return r"\cellcolor{gray!20}" + val

def to_latex_row(paper_key, paper):
    paper_info = paper["name"] + " \\cite{" + paper["key"] + "}"
    year = str(paper.get("year", ""))
    row = [paper_info]  # Year is now second column
    for field in assessment_fields:
        llm = format_value(paper["assessments"][field]["llm"]["value"])
        human = format_value(paper["assessments"][field]["manual"]["value"])
        # Check for mismatch (but ignore if both are "-")
        if llm != human:
            row.append(gray_cell(llm))
            row.append(gray_cell(human))
        else:
            row.append(llm)
            row.append(human)
    return " & ".join(row) + r" \\"

# Print LaTeX rows (sorted by year, then citation count)
records = []
for paper_title, paper in data.items():
    year = int(paper.get("year", 0))
    citation_count = int(paper.get("citation_count", 0))
    row = to_latex_row(paper_title, paper)
    records.append((-year, -citation_count, row))

records.sort()
for _, _, row in records:
    print(row)
    print("\\cline{2-15}")
