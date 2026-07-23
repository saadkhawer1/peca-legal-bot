import os
import sys
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from typing import TypedDict, List
from langgraph.graph import StateGraph, END
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import PromptTemplate
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from src.models import RetrievedChunk, ChatbotResponse
from src.retrieve import retrieve

load_dotenv()

# Define the State
class GraphState(TypedDict):
    query: str
    is_in_scope: bool
    retrieved_chunks: List[RetrievedChunk]
    answer: str
    sources: List[str]

# Initialize LLM
# Using Gemini 1.5 Flash for speed, or Pro if needed. We assume API key is in environment.
llm = ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0, max_retries=1)

# Schema for structured output during classification
class ScopeClassification(BaseModel):
    is_in_scope: bool = Field(description="True if the query is related to the Prevention of Electronic Crimes Act, 2016 (PECA) or Pakistani law regarding cybercrimes. False otherwise.")

# Node 1: Classify Query
def classify_query(state: GraphState) -> GraphState:
    query = state["query"]
    
    prompt = PromptTemplate(
        template="""You are a legal classifier. Determine if the following user query is asking about "The Prevention of Electronic Crimes Act, 2016" (PECA) of Pakistan, cybercrimes, or related legal matters.
        If the query is a general knowledge question (e.g., "what is chemistry?", "how to bake a cake") or about unrelated laws, classify it as out of scope.
        
        Query: {query}
        """,
        input_variables=["query"]
    )
    
    classifier_llm = llm.with_structured_output(ScopeClassification)
    chain = prompt | classifier_llm
    
    result = chain.invoke({"query": query})
    state["is_in_scope"] = result.is_in_scope
    return state

# Node 2: Retrieve Context
def retrieve_context(state: GraphState) -> GraphState:
    query = state["query"]
    chunks = retrieve(query, k=20)
    
    # We can also add a retrieval-score gating here if needed, but LLM classification is usually better.
    state["retrieved_chunks"] = chunks
    state["sources"] = list(set([c.source for c in chunks]))
    return state

from langchain_core.output_parsers import StrOutputParser

# Node 3: Generate Answer
def generate_answer(state: GraphState) -> GraphState:
    query = state["query"]
    chunks = state["retrieved_chunks"]
    
    context = "\n\n".join([f"--- Source: {c.source} ---\n{c.text}" for c in chunks])
    
    prompt = PromptTemplate(
        template="""You are a helpful legal assistant specializing in the Prevention of Electronic Crimes Act, 2016 (PECA) of Pakistan.
        Answer the user's question using ONLY the provided context. 
        If the answer is not contained in the context, explicitly say "I don't have enough information to answer that based on the PECA 2016 document."
        Always cite the source/page number from the context when making a claim.
        
        CRITICAL INSTRUCTION FOR READING LEGAL TEXTS:
        In Pakistani legal documents, a section (like "10. Cyber terrorism") often begins with a definition, followed by a list of conditions (a, b, c). The final penalty clause (e.g., "shall be punished with imprisonment...") at the very end of the list applies to the ENTIRE section/offence, even if the name of the offence isn't explicitly repeated in that final sentence. You must infer that the concluding penalty of a section applies to the offence defined at the start of that section.

        Context:
        {context}

        Question: {query}
        
        Answer:""",
        input_variables=["context", "query"]
    )
    
    chain = prompt | llm | StrOutputParser()
    answer_text = chain.invoke({"context": context, "query": query})
    
    state["answer"] = answer_text
    return state

# Conditional Edge
def check_scope(state: GraphState) -> str:
    if state["is_in_scope"]:
        return "retrieve_context"
    else:
        return "out_of_scope_response"

def out_of_scope_response(state: GraphState) -> GraphState:
    state["answer"] = "I can only answer questions about the Prevention of Electronic Crimes Act, 2016 (PECA). That question is outside what I have information on."
    state["sources"] = []
    return state

# Build the Graph
def build_graph():
    workflow = StateGraph(GraphState)
    
    # Add nodes
    workflow.add_node("classify_query", classify_query)
    workflow.add_node("retrieve_context", retrieve_context)
    workflow.add_node("generate_answer", generate_answer)
    workflow.add_node("out_of_scope_response", out_of_scope_response)
    
    # Add edges
    workflow.set_entry_point("classify_query")
    
    workflow.add_conditional_edges(
        "classify_query",
        check_scope,
        {
            "retrieve_context": "retrieve_context",
            "out_of_scope_response": "out_of_scope_response"
        }
    )
    
    workflow.add_edge("retrieve_context", "generate_answer")
    workflow.add_edge("generate_answer", END)
    workflow.add_edge("out_of_scope_response", END)
    
    return workflow.compile()

rag_app = build_graph()

def run_chat(query: str) -> ChatbotResponse:
    state = {"query": query, "is_in_scope": False, "retrieved_chunks": [], "answer": "", "sources": []}
    final_state = rag_app.invoke(state)
    
    return ChatbotResponse(
        answer=final_state["answer"],
        is_in_scope=final_state["is_in_scope"],
        sources=final_state["sources"]
    )

if __name__ == "__main__":
    resp = run_chat("What is the punishment for cyber terrorism?")
    print(f"In scope: {resp.is_in_scope}")
    print(f"Answer: {resp.answer}")
    print(f"Sources: {resp.sources}")
    
    print("\n--- Out of scope test ---")
    resp2 = run_chat("What is the capital of France?")
    print(f"In scope: {resp2.is_in_scope}")
    print(f"Answer: {resp2.answer}")
