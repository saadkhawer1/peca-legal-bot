import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import List
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from src.models import RetrievedChunk

DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def get_retriever():
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    return db.as_retriever(search_kwargs={"k": 4})

# use in graph.py
def retrieve(query: str, k: int = 20) -> List[RetrievedChunk]:
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")
    db = Chroma(persist_directory=DB_DIR, embedding_function=embeddings)
    
    # We use similarity_search_with_score to potentially use score-based gating
    docs_with_scores = db.similarity_search_with_score(query, k=k)
    
    # this function retrieves the most relevant legal sections from the ChromaDB
    # the chunks are then used to generate grounded responses using Google Gemini LLM
    chunks = []
    for doc, score in docs_with_scores:
        chunks.append(RetrievedChunk(
            text=doc.page_content,
            source=f"Page {doc.metadata.get('page', 'Unknown')}",
            score=float(score)
        ))
        
    return chunks

if __name__ == "__main__":
    # Task 4 test
    test_questions = [
        "What is cyber terrorism?",
        "What are the penalties for unauthorized access to an information system?",
        "How is a digital signature defined?"
    ]
    for q in test_questions:
        print(f"\n--- Question: {q} ---")
        chunks = retrieve(q, k=2)
        for i, c in enumerate(chunks):
            print(f"Chunk {i+1} (Source: {c.source}): {c.text[:150]}...")
