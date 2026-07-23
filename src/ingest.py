import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

# Path to the PDF
PDF_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "data", "PECA_2016.pdf")
DB_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "chroma_db")

def ingest_document():
    print(f"Loading document from {PDF_PATH}...")
    loader = PyPDFLoader(PDF_PATH)
    pages = loader.load()
    
    # Task 2: Document Loading & Chunking
    # Extract raw text
    full_text = "\n".join([page.page_content for page in pages])
    print(f"Total Character Count: {len(full_text)}")
    print(f"Total Word Count: {len(full_text.split())}")
    print(f"\n--- First 500 characters ---\n{full_text[:500]}\n---------------------------\n")

    # To prevent sentences that span across pages from being broken, we merge everything into one continuous string.
    combined_text = ""
    for p in pages:
        page_num = p.metadata.get("page", 0)
        # Replace newlines with spaces so paragraphs aren't arbitrarily broken
        clean_text = p.page_content.replace('\n', ' ')
        combined_text += f" [PAGE {page_num}] " + clean_text

    from langchain_core.documents import Document
    full_doc = Document(page_content=combined_text, metadata={"source": PDF_PATH})
    
    # Chunking
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2500,
        chunk_overlap=500,
        separators=[". ", " ", ""],
        length_function=len,
    )
    
    chunks = text_splitter.split_documents([full_doc])
    print(f"Split the document into {len(chunks)} chunks.")
    
    # Display 2-3 chunks for the report
    print("\n--- Sample Chunk 1 ---")
    print(chunks[0].page_content)
    print("\n--- Sample Chunk 2 ---")
    print(chunks[min(1, len(chunks)-1)].page_content)

    # Task 3: Embeddings & Vector Store
    # We use a free local sentence-transformers model
    print("\nInitializing embedding model (all-MiniLM-L6-v2)...")
    embeddings = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

    print(f"Storing chunks in Chroma vector store at {DB_DIR}...")
    db = Chroma.from_documents(chunks, embeddings, persist_directory=DB_DIR)
    
    print("Ingestion complete!")
    return db

def test_retrieval(db, query="What is cyber terrorism?"):
    print(f"\n--- Testing Retrieval for query: '{query}' ---")
    results = db.similarity_search(query, k=3)
    for i, res in enumerate(results):
        print(f"\nResult {i+1} (Source: {res.metadata.get('source')} Page: {res.metadata.get('page')}):")
        print(res.page_content[:200] + "...")

if __name__ == "__main__":
    db = ingest_document()
    test_retrieval(db)
