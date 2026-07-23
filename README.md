# 🇵🇰 RAG Chatbot on Pakistani Law (PECA 2016)

A Retrieval-Augmented Generation (RAG) chatbot that answers questions **only** about the **Prevention of Electronic Crimes Act (PECA), 2016** of Pakistan.

This project was developed as part of the **AI Summer Internship 2026** assignment. The chatbot retrieves relevant sections from the official PECA document using semantic search and generates grounded responses using Google's Gemini LLM. Unlike a traditional chatbot, it does not rely on general knowledge and only answers questions supported by the selected law.

---

# 📌 Project Objective

The goal of this project is to build a trustworthy legal chatbot using the Retrieval-Augmented Generation (RAG) architecture.

The chatbot:

- Reads the official PECA 2016 PDF
- Splits the document into meaningful chunks
- Converts chunks into vector embeddings
- Stores embeddings in ChromaDB
- Retrieves the most relevant legal sections
- Uses Google Gemini to generate grounded answers
- Rejects questions outside the scope of PECA

---

# 📚 Selected Law

**Law Name**

Prevention of Electronic Crimes Act (PECA), 2016

**Country**

Pakistan

**Document Source**

Official Ministry of Law and Justice, Government of Pakistan

**Document Format**

PDF

---

# 🚀 Technologies Used

| Technology | Purpose |
|------------|---------|
| Python | Programming Language |
| FastAPI | REST API Backend |
| LangChain | LLM Orchestration |
| LangGraph | Workflow Pipeline |
| Google Gemini 1.5 Flash | Large Language Model |
| HuggingFace MiniLM-L6-v2 | Text Embeddings |
| ChromaDB | Vector Database |
| Pydantic | Data Validation |
| HTML/CSS/JavaScript | Chat Frontend |
| Docker | Containerization |

---

# 🧠 What is RAG?

Retrieval-Augmented Generation (RAG) is an AI architecture that combines information retrieval with a Large Language Model.

Instead of allowing the model to answer from its own memory, the chatbot first retrieves the most relevant sections of the legal document and then generates an answer using only those sections.

This approach greatly reduces hallucinations and improves answer reliability.

---

# 🔄 System Architecture

```text
                User Question
                      │
                      ▼
             Scope Classification
                      │
        ┌─────────────┴─────────────┐
        │                           │
 Out of Scope                 In Scope
        │                           │
 Decline Response                  ▼
                           Retrieve Chunks
                                  │
                                  ▼
                         Chroma Vector Search
                                  │
                                  ▼
                         Relevant Legal Sections
                                  │
                                  ▼
                        Prompt Construction
                                  │
                                  ▼
                        Google Gemini 1.5 Flash
                                  │
                                  ▼
                       Grounded Final Response
                                  │
                                  ▼
                          FastAPI Response
```

---

# 📂 Project Structure

```text
PECA-RAG-Chatbot/
│
├── data/
│   └── PECA_2016.pdf
│
├── chroma_db/
│
├── src/
│   ├── ingest.py
│   ├── retriever.py
│   ├── graph.py
│   ├── schemas.py
│   ├── prompts.py
│   ├── embeddings.py
│   ├── main.py
│   └── utils.py
│
├── frontend/
│   ├── index.html
│   ├── style.css
│   └── script.js
│
├── tests/
│   └── eval.py
│
├── requirements.txt
├── Dockerfile
├── .gitignore
├── .env
└── README.md
```

---

# ⚙️ Installation

## 1. Clone Repository

```bash
git clone https://github.com/yourusername/PECA-RAG-Chatbot.git

cd PECA-RAG-Chatbot
```

---

## 2. Create Virtual Environment

```bash
python -m venv .venv
```

### Windows

```bash
.venv\Scripts\activate
```

### Linux / macOS

```bash
source .venv/bin/activate
```

---

## 3. Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 4. Create .env File

```env
GEMINI_API_KEY=your_api_key_here
```

---

# 📄 Document Ingestion

Run:

```bash
python src/ingest.py
```

This script performs:

- Loads the PECA PDF
- Extracts text
- Cleans the content
- Splits document into chunks
- Generates embeddings
- Stores vectors inside ChromaDB

---

# ✂️ Chunking Strategy

The chatbot uses **RecursiveCharacterTextSplitter** provided by LangChain.

Configuration:

```python
Chunk Size = 1000 Characters

Chunk Overlap = 200 Characters
```

### Why these values?

- Prevents legal clauses from breaking
- Preserves surrounding context
- Improves retrieval quality
- Reduces hallucinations

Natural separators such as paragraphs and line breaks are preferred over blind character splitting.

---

# 🧠 Embedding Model

Model Used

```
sentence-transformers/all-MiniLM-L6-v2
```

Advantages

- Free
- Lightweight
- Fast
- High semantic similarity performance

---

# 🗄️ Vector Database

Vector Store

```
ChromaDB
```

Stores:

- Embedding vectors
- Chunk metadata
- Page numbers
- Source references

---

# 🤖 LLM

Model

```
Google Gemini 1.5 Flash
```

Responsibilities

- Receives retrieved chunks
- Generates grounded responses
- Never answers outside retrieved context

---

# 🛡️ Scope Guardrails

The chatbot answers questions **only** about PECA 2016.

Out-of-scope examples:

- What is Chemistry?
- Who is Ronaldo?
- Explain Machine Learning.
- Tell me about Company Law.
- What is the capital of Pakistan?

Such questions receive a polite refusal instead of a fabricated answer.

---

# 📌 Features

- PDF-based knowledge retrieval
- Semantic search using embeddings
- Chroma vector database
- Google Gemini integration
- LangGraph workflow
- Source citations
- Scope guardrails
- Pydantic validation
- FastAPI backend
- Responsive chat interface
- Docker support

---

# 🌐 API Endpoints

## POST /ask

Request

```json
{
  "query": "What is cyber stalking?"
}
```

Response

```json
{
  "answer":"Cyber stalking is defined under...",
  "is_scope":true,
  "sources":[
      "Section 24",
      "Page 17"
  ]
}
```

---

## GET /health

Response

```json
{
  "status":"healthy"
}
```

---

# 💻 Running the Application

Start FastAPI

```bash
uvicorn src.main:app --reload
```

Open

```
http://localhost:8000
```

Swagger Documentation

```
http://localhost:8000/docs
```

---

# 🧪 Testing

Run

```bash
python tests/eval.py
```

Evaluation includes:

- 5 In-Scope Questions
- 3 Ambiguous Questions
- 5 Out-of-Scope Questions
- 2 Adversarial Questions

Metrics

- Scope Detection Accuracy
- Grounded Responses
- Source Citation Accuracy
- Retrieval Quality

---

# 🐳 Docker

Build Image

```bash
docker build -t peca-chatbot .
```

Run Container

```bash
docker run -p 8000:8000 --env-file .env peca-chatbot
```

---

# 📈 Future Improvements

- Hybrid Search (BM25 + Vector Search)
- Conversation Memory
- OCR Support for scanned legal documents
- Multi-law support
- User authentication
- Feedback collection
- Citation highlighting
- PDF upload functionality

---

# 👨‍💻 Author

AI Summer Internship 2026

Project:
**RAG Chatbot on Pakistani Law (PECA 2016)**

Built using LangChain, LangGraph, FastAPI, ChromaDB and Google Gemini.
