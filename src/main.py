import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import os
from pydantic import BaseModel

from src.models import QueryRequest, ChatbotResponse
from src.graph import run_chat

"""
Main Application Module
-----------------------
This module initializes the FastAPI server, mounts the static frontend,
and defines the core endpoints for the PECA 2016 RAG Chatbot.
"""

app = FastAPI(title="PECA 2016 RAG Chatbot")

# Mount static files
STATIC_DIR = os.path.join(os.path.dirname(os.path.dirname(__file__)), "static")
app.mount("/static", StaticFiles(directory=STATIC_DIR), name="static")

@app.get("/")
async def root():
    return FileResponse(os.path.join(STATIC_DIR, "index.html"))

@app.get("/health")
async def health_check():
    return {"status": "healthy", "model": "PECA 2016 RAG Chatbot"}

@app.post("/ask", response_model=ChatbotResponse)
async def ask_question(request: QueryRequest):
    try:
        response = run_chat(request.query)
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
