# RAG Chatbot on Pakistani Law (PECA 2016)

This project is a Retrieval-Augmented Generation (RAG) chatbot focused specifically on **The Prevention of Electronic Crimes Act, 2016 (PECA)** of Pakistan. It was built for the AI Summer Internship 2026.

## Technologies Used
- **Backend Framework:** FastAPI
- **LLM Orchestration:** LangChain & LangGraph
- **LLM:** Google Gemini 1.5 Flash (via `langchain-google-genai`)
- **Embeddings:** HuggingFace `sentence-transformers/all-MiniLM-L6-v2` (Local, free)
- **Vector Database:** ChromaDB
- **Validation:** Pydantic
- **Frontend:** Vanilla HTML/CSS/JS with a modern glassmorphism design.
- **Containerization:** Docker

## Setup Instructions

### 1. Prerequisites
- Python 3.10+
- A Google Gemini API Key

### 2. Installation
Clone the repository and install dependencies:
```bash
python -m venv .venv
# Activate environment
# On Windows:
.venv\Scripts\activate
# On Linux/Mac:
# source .venv/bin/activate

pip install -r requirements.txt
```

### 3. Environment Variables
Create a `.env` file in the root directory and add your API key:
```env
GEMINI_API_KEY=your_api_key_here
```

### 4. Data Ingestion
Run the ingestion script to load the PDF, chunk it, generate embeddings, and store them in ChromaDB.
```bash
python src/ingest.py
```
**Chunking Strategy:** I used `RecursiveCharacterTextSplitter` with natural legal boundaries (paragraphs, newlines) and a chunk size of 1000 characters with an overlap of 200 characters. This ensures legal clauses aren't split mid-sentence, preserving context.

### 5. Running the API & Chat UI
Start the FastAPI server:
```bash
uvicorn src.main:app --reload
```
Open `http://localhost:8000` in your browser to use the chatbot UI.

## Features
- **Strict Scope Guardrails:** A LangGraph pipeline classifies the user's intent before retrieval. If the query is out-of-scope (e.g., general knowledge), the bot politely declines.
- **Source Citations:** Every generated answer cites the specific chunks/pages retrieved from the PDF.
- **Structured Outputs:** Uses Pydantic for validating all requests and responses throughout the pipeline.

## API Endpoints
- `POST /ask`: Accepts a JSON body `{"query": "your question"}` and returns a grounded response, boolean scope flag, and sources list.
- `GET /health`: Returns `{ "status": "healthy" }`.

## Docker
To run using Docker:
```bash
docker build -t peca-chatbot .
docker run -p 8000:8000 --env-file .env peca-chatbot
```

## Testing
Run the evaluation suite (Task 8):
```bash
python tests/eval.py
```
This tests 15 questions covering in-scope, out-of-scope, tricky, and adversarial cases.
