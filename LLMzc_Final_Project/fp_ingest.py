import requests
from minsearch import Index
import pandas as pd

def load_qa_kb():
    # Load your CSV
    df = pd.read_csv("qa_knowledge_base.csv")
    
    qa_list = []
    
    for idx, data in df.iterrows():
        record = {
            "qa_id": data["qa_id"],
            "doc_id": data["doc_id"],
            "question": data["question"],
            "answer": data["answer"]
        }
        qa_list.append(record)
    
    return qa_list

def build_index(documents):
    index = Index(
        text_fields=["question", "answer"]
    )
    index.fit(documents)
    return index