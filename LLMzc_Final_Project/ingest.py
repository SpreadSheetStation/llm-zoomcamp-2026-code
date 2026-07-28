import requests
from minsearch import Index

def load_ground_truth():
    # Load your CSV
    df = pd.read_csv("ground_truth.csv")
    
    ground_truth_list = []
    
    for qa_id, data in ground_truth.items():
        doc_id = data["doc_id"]
        chunk_text = chunks[doc_id]
        
        record = {
            "qa_id": qa_id,
            "doc_id": doc_id,
            "chunk": chunk_text,
            "question": data["question"],
            "answer": data["answer"]
        }
        ground_truth_list.append(record)
    
    return ground_truth_list


def build_index(documents):
    index = Index(
        text_fields=["chunk", "question", "answer"]
    )
    index.fit(documents)
    return index