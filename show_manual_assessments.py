import json

def safe_get(d, *keys, default="N/A"):
    """Safely get nested dictionary values."""
    for k in keys:
        if not isinstance(d, dict) or k not in d:
            return default
        d = d[k]
    return d if d not in ("", None) else default


def show_manual_assessments(json_path):
    with open(json_path, "r", encoding="utf-8") as f:
        data = json.load(f)

    for paper_title, paper_info in data.items():
    

        assessments = paper_info.get("assessments", {})

        for metric_name, metric_data in assessments.items():
            

            manual1_value = safe_get(metric_data, "manual1", "value")
            manual1_why = safe_get(metric_data, "manual1", "why")

            manual_value = safe_get(metric_data, "manual", "value")
            manual_why = safe_get(metric_data, "manual", "why")

           
            if (manual_why == "N/A") and (manual1_why != "N/A"):

                print("=" * 40)
                print(f"Key: {paper_info['key']}")
                print("=" * 40)
                print(f"Metric: {metric_name}")
                print("-" * 40)
                print("manual1:")
                print(f"  value: {manual1_value}")
                print(f"  why  : {manual1_why}")

                print("\nmanual:")
                print(f"  value: {manual_value}")
                print(f"  why  : {manual_why}")

        print("\n")  # spacing between papers


if __name__ == "__main__":
    # Update this path to your JSON file
    json_file_path = "results/assessments.json"
    show_manual_assessments(json_file_path)
