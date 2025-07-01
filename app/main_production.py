# app/main_production.py
from fastapi import FastAPI, HTTPException, BackgroundTasks
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
import logging
import time
import uuid
from contextlib import asynccontextmanager

from app.core.config import settings
from app.services.deepseek_processor import deepseek_processor
from app.models.schemas import TextRequest, ProcessResult

# 配置日志
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时检查
    logger.info("🚀 AI学术润色系统启动")
    logger.info(f"✅ 火山引擎 API: {'已配置' if settings.ark_api_key else '未配置'}")
    logger.info(f"✅ 模型: {settings.deepseek_model_id}")
    yield
    # 关闭时的清理工作
    logger.info("🔒 应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title="AI学术润色系统",
    description="基于火山引擎DeepSeek-R1的专业学术文本润色服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS中间件配置（适配所有前端）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 开发阶段允许所有来源
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 请求日志中间件
@app.middleware("http")
async def log_requests(request, call_next):
    request_id = str(uuid.uuid4())[:8]
    start_time = time.time()
    
    logger.info(f"📝 请求 [{request_id}] {request.method} {request.url.path}")
    
    response = await call_next(request)
    
    process_time = time.time() - start_time
    logger.info(f"✅ 响应 [{request_id}] {response.status_code} - {process_time:.2f}s")
    
    response.headers["X-Request-ID"] = request_id
    return response

# 根路径
@app.get("/")
async def root():
    return {
        "message": "AI学术润色系统",
        "description": "专业的学术文本润色、AI检测和风格转换服务",
        "version": "1.0.0",
        "api_docs": "/docs",
        "status": "运行中",
        "powered_by": "火山引擎 DeepSeek-R1"
    }

# 健康检查
@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "ai-academic-polish",
        "api_provider": "ark_deepseek_r1",
        "model": settings.deepseek_model_id,
        "timestamp": int(time.time()),
        "version": "1.0.0"
    }

# 获取支持的风格
@app.get("/api/v1/styles")
async def get_styles():
    return {
        "styles": [
            {
                "id": "academic",
                "name": "学术论文",
                "description": "提高专业性和严谨性，适合学术论文和研究报告"
            },
            {
                "id": "formal", 
                "name": "正式文体",
                "description": "庄重得体的语言风格，适合正式文档和商务场合"
            },
            {
                "id": "casual",
                "name": "通俗易懂", 
                "description": "简洁明了的表达方式，便于普通读者理解"
            },
            {
                "id": "creative",
                "name": "创意表达",
                "description": "新颖有趣的表达方式，增强文本吸引力"
            }
        ]
    }

# 主要文本处理接口
@app.post("/api/v1/process", response_model=ProcessResult)
async def process_text(request: TextRequest):
    # 确保风格不为空
    style = request.style or "academic"
    logger.info(f"🔄 处理请求: {len(request.content)}字符, 风格: {style}")
    
    try:
        # 调用AI处理 - 添加详细日志和验证
        logger.debug(f"开始处理文本，长度: {len(request.content)}，风格: {style}")
        
        # 添加输入验证
        if not request.content or not isinstance(request.content, str):
            logger.error("无效的输入内容")
            raise HTTPException(status_code=400, detail="输入内容不能为空且必须是字符串")
        
        if style not in ["academic", "formal", "casual", "creative"]:
            logger.warning(f"未知风格: {style}，将使用默认学术风格")
            style = "academic"
        
        # 调用AI处理
        result = await deepseek_processor.process_text(request.content, style)
        
        # 验证结果结构
        required_keys = ["text", "ai_score", "processing_time"]
        if not all(key in result for key in required_keys):
            missing = [k for k in required_keys if k not in result]
            logger.error(f"AI返回结果缺少必要字段: {missing}")
            raise HTTPException(status_code=502, detail="AI服务返回无效响应")
        
        # 构建响应 - 添加更严格的类型检查
        try:
            response = ProcessResult(
                original_text=request.content,
                processed_text=str(result["text"]),  # 确保是字符串
                reasoning_content=str(result.get("reasoning", "无")),  # 默认值更明确
                ai_probability=float(result["ai_score"]),  # 确保是浮点数
                processing_time=float(result["processing_time"]),  # 确保是浮点数
                style_used=style,
                api_used=str(result.get("api_used", "unknown"))  # 确保是字符串
            )
        except (ValueError, TypeError) as e:
            logger.error(f"响应数据转换错误: {str(e)}")
            raise HTTPException(status_code=502, detail="AI服务返回数据格式错误")
        
        # 添加详细的成功日志
        logger.info(
            f"✅ 处理完成 - 字符数: {len(request.content)}→{len(response.processed_text)} "
            f"耗时: {response.processing_time:.2f}s "
            f"AI概率: {response.ai_probability:.2f}"
        )
        
        # 返回响应前添加调试日志
        if logger.isEnabledFor(logging.DEBUG):
            logger.debug(f"完整响应: {response.json(exclude={'original_text'})[:200]}...")
        
        return response
        
    except HTTPException:
        raise  # 直接抛出已有的HTTP异常
        
    except Exception as e:
        logger.exception("处理过程中出现未预期错误")  # 这会记录完整的堆栈跟踪
        raise HTTPException(
            status_code=500,
            detail=f"处理失败: {str(e)}"
        )

# AI检测接口
@app.post("/api/v1/detect")
async def detect_ai_text(request: TextRequest):
    """
    AI文本检测接口
    
    分析文本的AI生成概率
    """
    logger.info(f"🔍 AI检测请求: {len(request.content)}字符")
    
    try:
        # 这里可以集成专门的AI检测模型
        # 暂时使用简单的检测逻辑
        result = await deepseek_processor.process_text(request.content, "academic")
        
        return {
            "content": request.content,
            "ai_probability": result["ai_score"],
            "confidence_level": "medium" if result["ai_score"] > 0.5 else "low",
            "analysis": {
                "pattern_score": result["ai_score"] * 0.6,
                "complexity_score": result["ai_score"] * 0.4,
                "semantic_score": result["ai_score"] * 0.5
            },
            "processing_time": result["processing_time"]
        }
        
    except Exception as e:
        logger.error(f"❌ 检测失败: {str(e)}")
        raise HTTPException(status_code=500, detail="AI检测失败")

# 批量处理接口
@app.post("/api/v1/batch")
async def batch_process(
    requests: list[TextRequest], 
    background_tasks: BackgroundTasks
):
    """
    批量文本处理接口
    
    支持同时处理多个文本
    """
    if len(requests) > 10:
        raise HTTPException(status_code=400, detail="批量处理最多支持10个文本")
    
    logger.info(f"📦 批量处理: {len(requests)}个文本")
    
    try:
        results = []
        for i, req in enumerate(requests):
            logger.info(f"🔄 处理第{i+1}个文本...")
            style = req.style or "academic"
            result = await deepseek_processor.process_text(req.content, style)
            
            results.append({
                "index": i,
                "original_text": req.content,
                "processed_text": result["text"],
                "ai_probability": result["ai_score"],
                "processing_time": result["processing_time"],
                "style": req.style
            })
        
        total_time = sum(r["processing_time"] for r in results)
        logger.info(f"✅ 批量处理完成: {total_time:.2f}s")
        
        return {
            "total_count": len(results),
            "total_time": total_time,
            "results": results
        }
        
    except Exception as e:
        logger.error(f"❌ 批量处理失败: {str(e)}")
        raise HTTPException(status_code=500, detail="批量处理失败")

# 错误处理
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    logger.error(f"HTTP错误: {exc.status_code} - {exc.detail}")
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": True,
            "status_code": exc.status_code,
            "message": exc.detail,
            "timestamp": int(time.time())
        }
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    logger.error(f"未处理的错误: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "error": True,
            "status_code": 500,
            "message": "服务器内部错误",
            "timestamp": int(time.time())
        }
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main_production:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )