# FuzzCheck.AI: On the Limitations of DNN Fuzzing to Discover Security Failures

This repository contains all artifacts necessary to independently verify the results reported in the paper:

> **SoK: FuzzCheck.AI: On the Limitations of DNN Fuzzing to Discover Security Failures**

## Repository Structure

```bash
.
├── analysis
│   ├── assessment_llm_vs_human_table_8.py
│   ├── assessment_table_3.py
│   ├── evaluator_agreements.py
│   ├── llm_human_agreement_table_7.py
│   ├── metrics_vs_design_5.py
│   ├── metrics_vs_year_6.py
│   └── summary_table_4.py
├── codebook.json
├── llm_assessment_pipeline.py
├── papers
├── README.md
├── requirements.txt
└── results
    └── assessments.json
```

## Artifacts

### **Evaluation Codebook**
**File:** `codebook.json`  
Defines all *FuzzCheck.AI* metrics and the criteria for Low / Medium / High compliance. This codebook is used by both LLM assessment pipeline and human experts.

---

### **LLM-Assisted Preliminary Assessment Pipeline**
**File:** `llm_assessment_pipeline.py`  

Implements the LLM-assisted assessment procedure described in the paper. For each paper and each evaluation metric, the script:

- Independently queries two LLMs (ChatGPT and Gemini) using the full paper and the codebook definition.
- Requires each LLM to assign a compliance value and provide a justification with cited evidence (e.g., quotes, section names, or page references).
- Compares the two LLM outputs and accepts the result when they agree.
- Invokes a third LLM-based arbitration step only when the two models disagree.
- Stores all intermediate and arbitrated outputs to support subsequent expert review.

---

### **LLM-Generated Preliminary Assessments**
**File:** `results/assessments.json`  

For each evaluated paper and each *FuzzCheck.AI* metric, this file records the outputs produced by the LLM-assisted assessment pipeline, including:

- Independent assessments from two LLMs (ChatGPT and Gemini), each providing:
  - A proposed compliance value
  - A justification
  - Cited evidence from the paper (e.g., quotes, sections, or page references)
- An arbitrated LLM verdict produced by an arbitration step when the two models disagree


---

### **Expert-Validated and Corrected Final Assessments**
**File:** `results/assessments.json`  

For each paper and each *FuzzCheck.AI* metric, this file also contains the final assessments produced after expert review.  
During this process, human experts:

- Verify the LLM-extracted evidence against the paper and assess whether the provided rationale aligns with the codebook criteria.
- Correct compliance values when LLM assessments are inaccurate or inconsistent with the rubric.
- Provide human-authored justifications when corrections are made.

All empirical results and tables reported in the paper are computed from these expert-validated assessments.

---

### **Analysis Scripts**
**Directory:** `analysis/`  
Scripts used to generate the analysis tables reported in the paper:

- `assessment_table_3.py` — Generates the per-paper compliance matrix reporting each fuzzer's compliance level across all *FuzzCheck.AI* metrics (Table 3).

- `summary_table_4.py` — Computes the distribution of studies across High / Medium / Low compliance levels for each *FuzzCheck.AI* metric (Table 4).

- `metrics_vs_design_5.py` — Generates Table 5 by computing the percentage of studies at each compliance level for each fuzzing design choice (mutation strategy, exploration strategy, oracle type, and access level).

- `metrics_vs_year_6.py` — Generates Table 6 by computing year-wise distributions of High / Medium / Low compliance levels for each metric from 2017–2025.


- `llm_human_agreement_table_7.py` — Generates Table 7 by computing per-metric LLM–human agreement across the 32 evaluated papers.

- `assessment_llm_vs_human_table_8.py` — Generates Table 8, showing per-paper agreement between preliminary LLM-assisted labels and expert-corrected final labels across all metrics.

- `evaluator_agreements.py` — Computes how often the arbitrator and human experts adopt ChatGPT’s versus Gemini’s assessments in disagreement cases, to assess whether arbitration favors a particular LLM evaluator.

---

## LLM-Based Preliminary Assessment

```python
# 1) Put the DNN fuzzing research papers inside `papers` directory.

# 2) Create env (Python 3.10–3.12 recommended)
python -m venv .venv && source .venv/bin/activate

# 3) Install dependencies
pip install -r requirements.txt

# 4) Set OpenAI and Gemini API keys
export OPENAI_API_KEY=...
export GEMINI_API_KEY=...

# 5) Run LLM Assessment Pipeline
python llm_assessment_pipeline.py -p papers -c codebook.json -o results/assessments.json

```

