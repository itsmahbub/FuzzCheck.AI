import os
import json
import argparse
import re
from openai import OpenAI
from google import genai
from google.genai import types
import pathlib

OPENAI_MODEL = "o4-mini"
GEMINI_MODEL = "gemini-2.5-flash"

chatgpt_client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
gemini_client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

system_prompt = (
    "You are an expert in academic research analysis.\n\n"
    "You are given:\n"
    "1. One assessment metric definition specific to a research domain.\n"
    "2. The full text of a research paper.\n\n"
    "Your task is to evaluate the method proposed in the paper against this single metric.\n\n"
    "Instructions:\n"
    "- Base your reasoning strictly on the paper’s content. Do not infer or assume anything not explicitly stated.\n"
    "- Focus on technical and methodological sections (e.g., design, implementation, evaluation, dataset).\n"
    "- Assign one of the allowed values listed in the metric definition.\n"
    "- Explain why this value applies.\n"
    "- Provide direct evidence from the paper—quotes, section names, or page numbers.\n"
    "Output:\n"
    "- Return a JSON object wrapped in a markdown code block.\n"
    "- Follow this schema:\n"
    "```json\n"
    "{\n"
    "  \"value\": \"<value>\",\n"
    "  \"why\": \"Explanation of why this value was assigned\",\n"
    "  \"evidence\": \"<Page number, section name, and quote from the paper>\"\n"
    "}\n"
    "```"
)

def file_for_chatgpt(filename):
    file = chatgpt_client.files.create(
        file=open(filename, "rb"),
        purpose="user_data"
    )
    return file

def file_for_gemini(filename):
    return pathlib.Path(filename).read_bytes()

def read_assessment_metrics(json_path):
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)


def extract_llm_output(llm_response):
    try:
        return json.loads(llm_response)
    except json.JSONDecodeError:
        matches = re.findall(r"```json\s*(\{.*?\})\s*```", llm_response, re.DOTALL)
        for match in reversed(matches):
            try:
                return json.loads(match)
            except json.JSONDecodeError:
                continue
    raise ValueError("No valid JSON found in the response.")

def evaluate_with_model(model, paper_path, metric_name, metric_info):

    lines = []
    lines.append(f"{metric_name}: {metric_info['description']}")
    for val, desc in metric_info["values"].items():
        lines.append(f"- {val}: {desc}")
    metric_description = "\n".join(lines)

    if model == 'chatgpt':
        paper_file = file_for_chatgpt(paper_path)
        try:
            response = chatgpt_client.responses.create(
                model=OPENAI_MODEL,
                input=[
                    {"role": "system", "content": system_prompt},
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "input_text",
                                "text":  f"Assessment Metric:\n{metric_description}"
                            },
                            {
                                "type": "input_file",
                                "file_id": paper_file.id,
                            }
                        ]
                    }
                ]
            )
        except Exception as e:
            print(f"Error with ChatGPT: {e}")
            return "Error generating response"
        return response.output_text.strip()
    else:
        paper_content = file_for_gemini(paper_path)
        prompt =  (
            f"Assessment Metric:\n{metric_description}"
        )
        try:
            response = gemini_client.models.generate_content(
                model=GEMINI_MODEL,
                config=types.GenerateContentConfig(system_instruction=system_prompt),
                contents=[
                    types.Part.from_bytes(
                        data=paper_content,
                        mime_type='application/pdf',
                    ),
                    prompt
                ]
            )
            
        except Exception as e:
            print(f"Error with Gemini: {e}")
            return "Error generating response"
        return response.text.strip()

def reconcile(chat_output, gemini_output, paper_path, metric_name, metric_info):
    paper_file = file_for_chatgpt(paper_path)
    messages = [
        {"role": "system", "content": (
            "You are an expert evaluator resolving discrepancies between two LLM assessments.\n"
            "You are given:\n"
            "1. A metric definition.\n"
            "2. The full research paper text.\n"
            "3. Two LLM assessments with different verdicts.\n\n"
            "Instructions:\n"
            "- Carefully evaluate both assessments based on the metric and the paper.\n"
            "- Provide your own reasoning and conclusion.\n"
            "- Output should be a JSON object wrapped in a markdown code block.\n"
            "- Follow this format:\n"
            "```json\n"
            "{\n"
            "  \"value\": \"<value>\",\n"
            "  \"why\": \"Your detailed reasoning\",\n"
            "  \"evidence\": \"<Page number, section, or quote>\"\n"
            "}\n"
            "```"
        )},
        {
            "role": "user",
            "content": [
                {
                    "type": "input_text",
                    "text":  f"Metric: {metric_name}\nDescription: {metric_info['description']}\nPossible Values: {metric_info['values']}\n Feel free to assign different value that the list in possible values when appropriate"
                },
                {
                    "type": "input_file",
                    "file_id": paper_file.id,
                },
                {
                     "type": "input_text",
                     "text": f"Evaluator A output:\n{chat_output}"
                },
                {
                     "type": "input_text",
                     "text": f"Evaluator B output:\n{gemini_output}"
                }
            ]
        }
    
    ]
    response = chatgpt_client.responses.create(
        model=OPENAI_MODEL,
        input=messages
    )
    return response.output_text.strip()

def process_paper(paper_path, assessments, papers, results_dir, output_json_path, override=False, no_cache=False):
    paper_name = os.path.splitext(os.path.basename(paper_path))[0]
    

    if paper_name not in papers:
        print("Paper not found in assessments.json, skipping:", paper_name)
        os.remove(paper_path)
        return
    print(papers[paper_name]['name'])
    paper_key = papers[paper_name]["key"]
    if "assessments" not in papers[paper_name]:
        papers[paper_name]["assessments"] = {}

    for metric_name, metric_info in assessments.items():
        if not override and "arbitrator" in papers[paper_name]["assessments"].get(metric_name, {}):
            print(f"Skipping {paper_name} - {metric_name} (already exists)")
            continue

        chatgpt_file = os.path.join(results_dir, f"{paper_key}-{metric_name}.chatgpt")
        gemini_file = os.path.join(results_dir, f"{paper_key}-{metric_name}.gemini")
        reconciled_file = os.path.join(results_dir, f"{paper_key}-{metric_name}.reconciled")

        if not no_cache and os.path.exists(chatgpt_file):
            with open(chatgpt_file, "r", encoding="utf-8") as f:
                chat_output = f.read()
        else:
            chat_output = evaluate_with_model('chatgpt', paper_path, metric_name, metric_info)
            with open(chatgpt_file, "w", encoding="utf-8") as f:
                f.write(chat_output)

        if not no_cache and os.path.exists(gemini_file):
            with open(gemini_file, "r", encoding="utf-8") as f:
                gemini_output = f.read()
        else:
            gemini_output = evaluate_with_model('gemini', paper_path, metric_name, metric_info)
            with open(gemini_file, "w", encoding="utf-8") as f:
                f.write(gemini_output)

        try:
            chat_result = extract_llm_output(chat_output)
            gemini_result = extract_llm_output(gemini_output)
        except Exception:
            print(f"Skipping {paper_name} - {metric_name}: JSON parsing error")
            continue

        if chat_result["value"] == gemini_result["value"]:
            final_result = chat_result
        else:
            if not no_cache and os.path.exists(reconciled_file):
                with open(reconciled_file, "r", encoding="utf-8") as f:
                    reconciliation_response = f.read()
            else:
                reconciliation_response = reconcile(chat_output, gemini_output, paper_path, metric_name, metric_info)
                with open(reconciled_file, "w", encoding="utf-8") as f:
                    f.write(reconciliation_response)

            try:
                final_result = extract_llm_output(reconciliation_response)
            except:
                print(f"Skipping {paper_name} - {metric_name}: Reconciliation failed")
                continue


        papers[paper_name].setdefault("assessments", {}).setdefault(metric_name, {})
        papers[paper_name]["assessments"][metric_name]["chatgpt"] = chat_result
        papers[paper_name]["assessments"][metric_name]["gemini"] = gemini_result
        papers[paper_name]["assessments"][metric_name]["arbitrator"] = final_result
        papers[paper_name]["assessments"][metric_name].setdefault("manual", {
            "value": "",
            "why": "",
            "evidence": ""
        })

        with open(output_json_path, "w", encoding="utf-8") as f:
            json.dump(papers, f, indent=4)
        print(f"Saved assessment for {paper_name} - {metric_name}")

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--paper-directory", default="papers")
    parser.add_argument("-c", "--codebook", default="codebook.json")
    parser.add_argument("-o", "--output-json", default="results/assessments.json")
    parser.add_argument("--override", action="store_true")
    parser.add_argument("--no-cache", action="store_true")
    args = parser.parse_args()

    results_dir = "llm_responses"
    os.makedirs(results_dir, exist_ok=True)

    if os.path.exists(args.output_json):
        with open(args.output_json, "r", encoding="utf-8") as f:
            papers = json.load(f)
    else:
        papers = {}

    assessments = read_assessment_metrics(args.codebook)

    paper_paths = [os.path.join(args.paper_directory, f) for f in os.listdir(args.paper_directory) if f.endswith(".pdf")]

    for paper_path in paper_paths:
        process_paper(
            paper_path,
            assessments,
            papers,
            results_dir,
            args.output_json,
            override=args.override,
            no_cache=args.no_cache
        )

if __name__ == "__main__":
    main()
