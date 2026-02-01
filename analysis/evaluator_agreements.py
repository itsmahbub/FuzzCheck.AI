"""
Computes arbitrator and human alignment with ChatGPT vs. Gemini in disagreement cases.
"""

import json

# Load file
with open("results/assessments.json") as f:
    data = json.load(f)

metrics = [
    "Failure Severity",
    "Targeted Attack Discovery",
    "Input Plausibility",
    "Failure Reproducibility",
    "Failure Diagnostics",
    "Attack Transferability"
]

# Counters
total = 0
overall = 0
arb_chat = arb_gem = man_chat = man_gem = 0

for entry in data.values():
    for metric in metrics:
        m = entry["assessments"][metric]
        arb = m.get("arbitrator", {}).get("value", "").lower()
        chat = m.get("chatgpt", {}).get("value", "").lower()
        gem = m.get("gemini", {}).get("value", "").lower()
        manual = m.get("manual", {}).get("value", "").lower()
        overall +=1
        if manual == chat:
            man_chat += 1
        if manual == gem:
            man_gem += 1
        if chat==gem: # No arbitration needed
            continue
        total += 1
        if arb == chat:
            arb_chat += 1
        if arb == gem:
            arb_gem += 1
        

# Results
print("=== Overall Agreement Across All Metrics ===")
print(f"Total comparisons: {total}")
print(f"Arbitrator = ChatGPT : {arb_chat/total*100:.1f}%")
print(f"Arbitrator = Gemini  : {arb_gem/total*100:.1f}%")
print(f"Manual = ChatGPT     : {man_chat/overall*100:.1f}%")
print(f"Manual = Gemini      : {man_gem/overall*100:.1f}%")
