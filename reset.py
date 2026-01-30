import json

REMOVE_KEYS = {"chatgpt", "gemini", "arbitrator"}

def clean_assessments(data):
    for paper in data.values():
        assessments = paper.get("assessments", {})
        for metric, entries in assessments.items():
            # Remove unwanted keys
            for k in list(entries.keys()):
                if k in REMOVE_KEYS:
                    del entries[k]

            # Rename manual -> manual1
            if "manual" in entries:
                entries["manual1"] = entries.pop("manual")

    return data


if __name__ == "__main__":
    # Load input JSON
    with open("results/assessments.json", "r") as f:
        data = json.load(f)

    # Clean
    data = clean_assessments(data)

    # Save output
    with open("results/assessments_cleaned.json", "w") as f:
        json.dump(data, f, indent=2)

    print("Done: chatgpt/gemini/arbitrator removed, manual → manual1")
