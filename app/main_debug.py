from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import logging
import os
from dotenv import load_dotenv

# 显式加载环境变量
load_dotenv()

# 配置详细日志
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

# 调试环境变量
logger.info("=== 火山引擎环境变量调试信息 ===")
logger.info(f"ARK_API_KEY: {'已设置' if os.getenv('ARK_API_KEY') else '未设置'}")
logger.info(f"ARK_BASE_URL: {os.getenv('ARK_BASE_URL')}")
logger.info(f"DEEPSEEK_MODEL_ID: {os.getenv('DEEPSEEK_MODEL_ID')}")

from app.core.config import settings
from app.services.deepseek_processor import deepseek_processor
from app.models.schemas import TextRequest, ProcessResult

app = FastAPI(
    title="AI学术润色系统 - 火山引擎版",
    description="火山引擎 DeepSeek-R1 API集成版本",
    version="1.0.0-ark"
)

# CORS配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    return {
        "message": "AI学术润色系统 - 火山引擎版",
        "ark_api_configured": bool(settings.ark_api_key),
        "api_key_preview": settings.ark_api_key[:10] + "..." if settings.ark_api_key else None,
        "ark_base_url": settings.ark_base_url,
        "model_id": settings.deepseek_model_id
    }

@app.get("/debug/env")
async def debug_env():
    """调试环境变量"""
    return {
        "ark_api_key_set": bool(settings.ark_api_key),
        "ark_api_key_length": len(settings.ark_api_key) if settings.ark_api_key else 0,
        "ark_base_url": settings.ark_base_url,
        "deepseek_model_id": settings.deepseek_model_id,
        "all_env_keys": [k for k in os.environ.keys() if 'API' in k or 'ARK' in k or 'DEEPSEEK' in k]
    }

@app.post("/api/v1/process", response_model=ProcessResult)
async def process_text(request: TextRequest):
    """文本处理接口"""
    logger.info(f"收到处理请求: {request.content[:50]}...")
    
    try:
        result = await deepseek_processor.process_text(request.content, request.style)
        
        return ProcessResult(
            original_text=request.content,
            processed_text=result["text"],
            ai_probability=result["ai_score"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        logger.error(f"处理错误: {e}")
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "api_service": "ark_deepseek",
        "api_configured": "yes" if settings.ark_api_key else "no",
        "model": settings.deepseek_model_id,
        "version": "1.0.0-ark"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app.main_debug:app", host="0.0.0.0", port=8000, reload=True)
