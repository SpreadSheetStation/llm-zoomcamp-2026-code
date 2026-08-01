import pandas as pd
from tqdm.auto import tqdm
from fp_ingest import load_qa_kb, build_index
from fp_rag_helper import RAGBase
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Load data
documents = load_qa_kb()
index = build_index(documents)

# Create the RAG assistant
assistant = RAGBase(
    index=index,
    llm_client=client,
    model="gpt-5.4-mini"
)

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
    
    answer_llm = assistant.rag(question)
    original_doc = doc_lookup[doc_id]
    answer_orig = original_doc["answer"]
    
    results.append({
        "question": question,
        "answer_llm": answer_llm,
        "answer_orig": answer_orig,
        "document": doc_id
    })

# Save results
df_results = pd.DataFrame(results)
df_results.to_csv("GroundTruth/rag_answers.csv", index=False)
print(f"Saved {len(results)} RAG answers to GroundTruth/rag_answers.csv")