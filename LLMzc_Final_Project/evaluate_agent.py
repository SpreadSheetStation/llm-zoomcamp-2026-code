import pandas as pd
from tqdm.auto import tqdm
from fp_ingest import load_qa_kb, build_index
from agentic_assistant import AgenticRAG
from dotenv import load_dotenv

load_dotenv()

# Load data and create the agent
documents = load_qa_kb()
index = build_index(documents)
agent = AgenticRAG(index)

# Load ground truth
df_gt = pd.read_csv("GroundTruth/my_ground_truth.csv")
ground_truth = df_gt.to_dict(orient="records")

# Create a lookup for original answers
doc_lookup = {}
for doc in documents:
    doc_lookup[doc["qa_id"]] = doc

# Generate answers
results = []
for rec in tqdm(ground_truth):
    question = rec["question"]
    doc_id = rec["document"]
    
    answer_agent = agent.ask(question)
    original_doc = doc_lookup[doc_id]
    answer_orig = original_doc["answer"]
    
    results.append({
        "question": question,
        "answer_agent": answer_agent,
        "answer_orig": answer_orig,
        "document": doc_id
    })

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv("GroundTruth/agent_answers.csv", index=False)
print(f"Saved {len(results)} agent answers to GroundTruth/agent_answers.csv")