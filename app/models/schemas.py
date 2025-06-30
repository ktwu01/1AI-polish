from pydantic import BaseModel, Field, field_validator
from typing import Optional, Literal
from datetime import datetime

class TextRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000, description="要处理的文本内容")
    style: Optional[str] = Field(default="academic", description="润色风格")
    
    @field_validator('style')
    @classmethod
    def validate_style(cls, v):
        """验证和标准化风格参数"""
        if v is None:
            return "academic"
        
        valid_styles = ["academic", "formal", "casual", "creative"]
        v = v.lower().strip()
        
        if v not in valid_styles:
            raise ValueError(f"风格必须是以下之一: {', '.join(valid_styles)}")
        
        return v

class ProcessResult(BaseModel):
    original_text: str = Field(..., description="原始文本")
    processed_text: str = Field(..., description="处理后的文本")
    reasoning_content: Optional[str] = Field(None, description="AI思考过程")  # 新增
    ai_probability: float = Field(..., ge=0.0, le=1.0, description="AI生成概率")
    processing_time: float = Field(..., ge=0.0, description="处理时间（秒）")
    style_used: Optional[str] = Field(None, description="使用的润色风格")
    api_used: Optional[str] = Field(None, description="使用的API服务")

class AsyncTaskResponse(BaseModel):
    task_id: str = Field(..., description="任务ID")
    status: str = Field(..., description="任务状态")
    message: Optional[str] = Field(None, description="状态消息")

class ProcessingHistoryResponse(BaseModel):
    id: int
    user_id: str
    original_text: str
    processed_text: str
    ai_probability: float
    processing_time: float
    created_at: datetime
    
    model_config = {"from_attributes": True}

class BatchProcessRequest(BaseModel):
    texts: list[TextRequest] = Field(..., description="批量处理的文本列表")

class AIDetectionRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000, description="要检测的文本内容")

class AIDetectionResult(BaseModel):
    content: str = Field(..., description="检测的文本")
    ai_probability: float = Field(..., ge=0.0, le=1.0, description="AI生成概率")
    confidence_level: Literal["low", "medium", "high"] = Field(..., description="置信度等级")
    analysis: dict = Field(..., description="详细分析结果")
    processing_time: float = Field(..., ge=0.0, description="处理时间（秒）")

class StyleInfo(BaseModel):
    id: str = Field(..., description="风格ID")
    name: str = Field(..., description="风格名称")
    description: str = Field(..., description="风格描述")
    
class StylesResponse(BaseModel):
    styles: list[StyleInfo] = Field(..., description="支持的风格列表")
