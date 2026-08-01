import pandas as pd
import numpy as np
from fp_ingest import load_qa_kb, build_index
from tqdm.auto import tqdm

# --- Load your ground truth ---
def load_ground_truth():
    df = pd.read_csv("GroundTruth/my_ground_truth.csv")
    return df.to_dict(orient="records")

# --- Load the search index ---
documents = load_qa_kb()
index = build_index(documents)

# --- Create a lookup to find documents by qa_id ---
doc_lookup = {}
for doc in documents:
    doc_lookup[doc["qa_id"]] = doc

# --- Search function with configurable boosts ---
def search_boosts(query, question_boost, answer_boost):
    boost_dict = {"question": question_boost, "answer": answer_boost}
    return index.search(query, num_results=5, boost_dict=boost_dict)

# --- Compute relevance for one query ---
def compute_relevance(q, search_function):
    correct_doc_id = q["document"]   # This is the qa_id
    results = search_function(query=q["question"])
    
    relevance = []
    for doc in results:
        # Check if the retrieved doc has the correct qa_id
        relevance.append(1 if doc["qa_id"] == correct_doc_id else 0)
    return relevance

# --- Compute relevance for all queries ---
def compute_relevance_total(ground_truth, search_function):
    relevance_total = []
    for q in tqdm(ground_truth):
        relevance = compute_relevance(q, search_function)
        relevance_total.append(relevance)
    return relevance_total

# --- Metrics: Hit Rate ---
def hit_rate(relevance_total):
    hits = 0
    for line in relevance_total:
        if 1 in line:
            hits += 1
    return hits / len(relevance_total)

# --- Metrics: Mean Reciprocal Rank (MRR) ---
def mrr(relevance_total):
    total_score = 0.0
    for line in relevance_total:
        for rank in range(len(line)):
            if line[rank] == 1:
                total_score += 1 / (rank + 1)
                break
    return total_score / len(relevance_total)

# --- Evaluate a search function ---
def evaluate(search_function):
    ground_truth = load_ground_truth()
    relevance_total = compute_relevance_total(ground_truth, search_function)
    return {
        "hit_rate": hit_rate(relevance_total),
        "mrr": mrr(relevance_total)
    }

# --- Test multiple boost combinations ---
if __name__ == "__main__":
    print("Testing different boost combinations...\n")
    
    boost_combinations = [
        {"name": "Default (q=2.0, a=0.5)", "q": 2.0, "a": 0.5},
        {"name": "Equal (q=1.0, a=1.0)", "q": 1.0, "a": 1.0},
        {"name": "High Question (q=3.0, a=0.5)", "q": 3.0, "a": 0.5},
        {"name": "High Answer (q=1.0, a=2.0)", "q": 1.0, "a": 2.0},
        {"name": "Very High Question (q=5.0, a=0.5)", "q": 5.0, "a": 0.5},
        {"name": "Very High Answer (q=1.0, a=4.0)", "q": 1.0, "a": 4.0},
    ]
    
    results_list = []
    
    for combo in boost_combinations:
        print(f"Testing: {combo['name']}")
        
        def search_fn(query, q=combo['q'], a=combo['a']):
            return search_boosts(query, question_boost=q, answer_boost=a)
        
        results = evaluate(search_fn)
        results_list.append({
            "name": combo['name'],
            "question_boost": combo['q'],
            "answer_boost": combo['a'],
            "hit_rate": results['hit_rate'],
            "mrr": results['mrr']
        })
        print(f"  Hit Rate: {results['hit_rate']:.4f}, MRR: {results['mrr']:.4f}\n")
    
    # Find the best combination
    df_results = pd.DataFrame(results_list)
    best_mrr = df_results.loc[df_results['mrr'].idxmax()]
    print("=" * 50)
    print(f"🏆 BEST COMBINATION: {best_mrr['name']}")
    print(f"   Hit Rate: {best_mrr['hit_rate']:.4f}")
    print(f"   MRR: {best_mrr['mrr']:.4f}")