from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class TextRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    style: Optional[str] = "academic"

class ProcessResult(BaseModel):
    original_text: str
    processed_text: str
    ai_probability: float
    processing_time: float

class AsyncTaskResponse(BaseModel):
    task_id: str
    status: str
    message: Optional[str] = None

class ProcessingHistoryResponse(BaseModel):
    id: int
    user_id: str
    original_text: str
    processed_text: str
    ai_probability: float
    processing_time: float
    created_at: datetime
    
    class Config:
        from_attributes = True
