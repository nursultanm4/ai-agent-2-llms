from pydantic import BaseModel, Field
from typing import Optional, Dict, Any

class QueryRequest(BaseModel):
    query: str = Field(..., min_length=1, max_length=1000, description="User's question or request")

class QueryResponse(BaseModel):
    answer: str = Field(..., description="AI generated response")
    meta: Dict[str, Any] = Field(..., description="Metadata about the response")

class HealthResponse(BaseModel):
    status: str = Field(..., description="Service status")
    timestamp: str = Field(..., description="Current timestamp")