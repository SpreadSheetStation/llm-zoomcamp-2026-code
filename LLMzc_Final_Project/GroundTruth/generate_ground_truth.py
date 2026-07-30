import os
import json
import time
import pandas as pd
from pydantic import BaseModel
from dotenv import load_dotenv
from openai import OpenAI
from concurrent.futures import ThreadPoolExecutor

# --- Import your data loader ---
# We need to go up one folder to find fp_ingest.py
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# Make Python look for files in the parent folder
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from fp_ingest import load_qa_kb

# --- 1. Define the output structure ---
class Questions(BaseModel):
    questions: list[str]

# --- 2. Instructions for the LLM ---
data_gen_instructions = """
You emulate a student who is studying the Dancing Plague of 1518.
Formulate 5 questions this student might ask based on a FAQ record. The record
should contain the answer to the questions, and the questions should be complete and not too short.
If possible, use as fewer words as possible from the record.

The output should resemble how people ask questions on the internet. Not too formal, not too short, not too long.
""".strip()

# --- 3. Helper functions ---
def llm_structured(client, instructions, user_prompt, output_type, model="gpt-5.4-mini"):
    messages = [
        {"role": "developer", "content": instructions},
        {"role": "user", "content": user_prompt}
    ]
    response = client.responses.parse(
        model=model,
        input=messages,
        text_format=output_type
    )
    return response.output_parsed, response.usage

def llm_structured_retry(client, instructions, user_prompt, output_type, model="gpt-5.4-mini", max_retries=3):
    for attempt in range(max_retries):
        try:
            return llm_structured(client, instructions, user_prompt, output_type, model=model)
        except Exception:
            if attempt == max_retries - 1:
                raise
            time.sleep(2 ** attempt)

def calc_price(usage):
    input_price_per_million = 0.75
    output_price_per_million = 4.50
    input_cost = (usage.input_tokens / 1_000_000) * input_price_per_million
    output_cost = (usage.output_tokens / 1_000_000) * output_price_per_million
    return {"total_cost": input_cost + output_cost}

def calc_total_price(usages):
    total_cost = 0.0
    for usage in usages:
        cost = calc_price(usage)
        total_cost = total_cost + cost["total_cost"]
    return total_cost

def map_progress(pool, seq, f):
    from tqdm.auto import tqdm
    results = []
    with tqdm(total=len(seq)) as progress:
        futures = []
        for el in seq:
            future = pool.submit(f, el)
            future.add_done_callback(lambda p: progress.update())
            futures.append(future)
        for future in futures:
            result = future.result()
            results.append(result)
    return results

# --- 4. The main generation function ---
def generate_ground_truth(doc):
    user_prompt = json.dumps(doc)
    out, usage = llm_structured_retry(
        openai_client,
        data_gen_instructions,
        user_prompt,
        Questions
    )
    results = []
    for q in out.questions:
        results.append({
            "question": q,
            "document": doc["qa_id"]   # We use qa_id as the document identifier
        })
    return results, usage

# --- 5. Run it ---
if __name__ == "__main__":
    # Load environment variables
    load_dotenv()
    openai_client = OpenAI()

    # Load your knowledge base
    print("Loading knowledge base...")
    # Change the working directory to the parent folder so the CSV can be found
    os.chdir(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    documents = load_qa_kb()
    print(f"Loaded {len(documents)} documents")

    # Generate ground truth in parallel
    print("Generating questions...")
    with ThreadPoolExecutor(max_workers=6) as pool:
        results = map_progress(pool, documents, generate_ground_truth)

    # Collect results
    ground_truth = []
    usages = []
    for records, usage in results:
        ground_truth.extend(records)
        usages.append(usage)

    # Save to CSV
    df_ground_truth = pd.DataFrame(ground_truth)
    # Get the path to the folder where this script is located
    script_dir = os.path.dirname(os.path.abspath(__file__))
    output_path = os.path.join(script_dir, "my_ground_truth.csv")
    df_ground_truth.to_csv(output_path, index=False)
    print(f"Saved {len(ground_truth)} questions to my_ground_truth.csv")

    # Print cost
    total_cost = calc_total_price(usages)
    print(f"Total cost: ${total_cost:.6f}")