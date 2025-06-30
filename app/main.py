from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import logging
from contextlib import asynccontextmanager

from app.core.config import settings
from app.api.v1.endpoints import router as api_v1_router
from app.models.database import create_tables

# 配置日志
logging.basicConfig(
    level=getattr(logging, settings.debug and "DEBUG" or "INFO"),
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时创建数据库表
    logger.info("创建数据库表...")
    create_tables()
    logger.info("应用启动完成")
    yield
    # 关闭时的清理工作
    logger.info("应用关闭")

# 创建FastAPI应用
app = FastAPI(
    title=settings.app_name,
    description="为学生提供AI写作润色、查重检测和降重处理服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    lifespan=lifespan
)

# CORS中间件配置（适配Vue前端）
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],  # Vue开发服务器
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册API路由
app.include_router(api_v1_router, prefix="/api/v1", tags=["AI处理"])

# 根路径
@app.get("/")
async def root():
    return {
        "message": f"欢迎使用{settings.app_name}",
        "docs": "/docs",
        "version": "1.0.0"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.debug
    )
