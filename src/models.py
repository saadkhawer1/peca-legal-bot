from pydantic import BaseModel, Field
from typing import List, Optional

# pydantic models for type safety and validation and also check the format of data
class QueryRequest(BaseModel):
    query: str = Field(..., description="The user's question about the PECA 2016 law.")

class RetrievedChunk(BaseModel):
    text: str = Field(..., description="The text content of the retrieved chunk.")
    source: str = Field(..., description="The source of the chunk, typically the PDF name or page.")
    score: Optional[float] = Field(None, description="The similarity score of the chunk if available.")

class ChatbotResponse(BaseModel):
    answer: str = Field(..., description="The generated answer to the user's query.")
    is_in_scope: bool = Field(..., description="Whether the query was classified as in-scope for the PECA 2016 law.")
    sources: List[str] = Field(default_factory=list, description="A list of sources cited in the answer.")
