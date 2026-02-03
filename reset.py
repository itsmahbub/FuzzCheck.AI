import json

REMOVE_KEYS = {"chatgpt", "gemini", "arbitrator"}

def clean_assessments(data):
    for paper in data.values():
        assessments = paper.get("assessments", {})
        for metric, entries in assessments.items():
            if metric == "Input Plausibility":
                # Remove unwanted keys
                for k in list(entries.keys()):
                    if k in REMOVE_KEYS:
                        del entries[k]
    return data


if __name__ == "__main__":
    # Load input JSON
    with open("results/assessments.json", "r") as f:
        data = json.load(f)

    # Clean
    data = clean_assessments(data)

    # Save output
    with open("results/assessments.json", "w") as f:
        json.dump(data, f, indent=4)

    print("Done: manual1")
