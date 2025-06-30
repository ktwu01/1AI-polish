# 临时简化版本 - app/main_simple.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import time

# 简化配置
class Settings:
    app_name = "AI学术润色系统"
    debug = True
    
settings = Settings()

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="为学生提供AI写作润色、查重检测和降重处理服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件配置（适配Vue前端）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TextRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000)
    style: Optional[str] = "academic"

class ProcessResult(BaseModel):
    original_text: str
    processed_text: str
    ai_probability: float
    processing_time: float

# 模拟AI处理函数
async def mock_ai_processing(text: str, style: str = "academic") -> dict:
    # 模拟处理延迟
    await asyncio.sleep(0.5)
    
    # 简单的风格处理
    style_prefixes = {
        "academic": "[学术润色]",
        "formal": "[正式润色]", 
        "casual": "[通俗润色]",
        "creative": "[创意润色]"
    }
    
    prefix = style_prefixes.get(style, "[默认润色]")
    processed_text = f"{prefix} {text.replace('人工智能', 'AI技术')}"
    
    # 模拟AI概率计算
    import random
    ai_score = random.uniform(0.1, 0.4)
    
    return {
        "text": processed_text,
        "ai_score": ai_score
    }

# API路由
@app.get("/")
async def root():
    return {
        "message": f"欢迎使用{settings.app_name}",
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI学术润色系统",
        "version": "1.0.0"
    }

@app.post("/api/v1/process", response_model=ProcessResult)
async def process_text(request: TextRequest):
    """文本处理接口"""
    start_time = time.time()
    
    # 处理文本
    result = await mock_ai_processing(request.content, request.style)
    
    end_time = time.time()
    processing_time = end_time - start_time
    
    return ProcessResult(
        original_text=request.content,
        processed_text=result["text"],
        ai_probability=result["ai_score"],
        processing_time=processing_time
    )

@app.post("/api/v1/process/async")
async def async_process_text(request: TextRequest):
    """异步文本处理接口（简化版本）"""
    import hashlib
    
    task_id = hashlib.md5(
        f"{request.content}_{request.style}".encode()
    ).hexdigest()
    
    return {
        "task_id": task_id,
        "status": "processing",
        "message": "任务已提交，请稍后查询结果"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_simple:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
