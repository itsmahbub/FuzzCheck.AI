"""
Find all cases where the manual (expert) assessment disagrees with the arbitrator LLM assessment.
Usage: python3 analysis/manual_vs_arbitrator_disagreements.py
"""

import json
from collections import Counter

ASSESSMENTS_FILE = 'results/assessments.json'

with open(ASSESSMENTS_FILE) as f:
    data = json.load(f)

disagreements = []

for paper_title, paper_data in data.items():
    assessments = paper_data.get('assessments', {})
    for metric, vals in assessments.items():
        manual_val = (vals.get('manual', {}).get('value', '') or '').strip()
        arb_val = (vals.get('arbitrator', {}).get('value', '') or '').strip()

        if not manual_val or not arb_val:
            continue
        if manual_val.lower() == arb_val.lower():
            continue

        disagreements.append({
            'paper': paper_data.get('name', paper_title),
            'key': paper_data.get('key', ''),
            'year': paper_data.get('year', ''),
            'metric': metric,
            'manual': manual_val,
            'arbitrator': arb_val,
            'chatgpt': (vals.get('chatgpt', {}).get('value', '') or ''),
            'gemini': (vals.get('gemini', {}).get('value', '') or ''),
            'manual_why': (vals.get('manual', {}).get('why', '') or ''),
            'arb_why': (vals.get('arbitrator', {}).get('why', '') or ''),
        })

print("Total disagreements (manual != arbitrator): %d" % len(disagreements))
print("=" * 90)

for i, d in enumerate(disagreements, 1):
    print("\n[%d] %s (%s) [%s]" % (i, d['paper'], d['year'], d['key']))
    print("    Metric:         %s" % d['metric'])
    print("    Manual:         %s" % d['manual'])
    print("    Arbitrator:     %s" % d['arbitrator'])
    print("    ChatGPT:        %s" % d['chatgpt'])
    print("    Gemini:         %s" % d['gemini'])
    print("    Manual why:     %s" % (d['manual_why'][:250] if d['manual_why'] else 'N/A'))
    print("    Arbitrator why: %s" % (d['arb_why'][:250] if d['arb_why'] else 'N/A'))
    print("-" * 90)

print("\n\nSUMMARY BY METRIC:")
for metric, count in sorted(Counter(d['metric'] for d in disagreements).items()):
    print("  %-35s %d disagreement(s)" % (metric + ':', count))

print("\nDIRECTION (manual -> arbitrator):")
for direction, count in sorted(
    Counter("%s -> %s" % (d['manual'], d['arbitrator']) for d in disagreements).items(),
    key=lambda x: -x[1]
):
    print("  %-25s %d" % (direction, count))
