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
arb_chat = arb_gem = man_chat = man_gem = chat_gem = chat_gem_diff = 0 

for entry in data.values():
    for metric in metrics:
        m = entry["assessments"][metric]
        arb = m.get("arbitrator", {}).get("value", "").lower()
        chat = m.get("chatgpt", {}).get("value", "").lower()
        gem = m.get("gemini", {}).get("value", "").lower()
        manual = m.get("manual", {}).get("value", "").lower()
        if manual == chat:
            man_chat += 1
        if manual == gem:
            man_gem += 1
        if chat==gem:
            chat_gem +=1
        total += 1
        if chat != gem:
            chat_gem_diff += 1
            if arb == chat:
                arb_chat += 1
            if arb == gem:
                arb_gem += 1
        

# Results
print("=== Overall Agreement Across All Metrics ===")
print(f"Total comparisons: {total}")
print(f"LLM evaluator disagreements: {chat_gem_diff}")
print(f"LLM evaluator agreements: {total-chat_gem_diff}")
print(f"Arbitrator = ChatGPT : {arb_chat/chat_gem_diff*100:.1f}%")
print(f"Arbitrator = Gemini  : {arb_gem/chat_gem_diff*100:.1f}%")
print(f"Manual = ChatGPT     : {man_chat/total*100:.1f}%")
print(f"Manual = Gemini      : {man_gem/total*100:.1f}%")
