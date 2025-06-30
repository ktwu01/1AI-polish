from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from sqlalchemy.orm import Session
import asyncio
import hashlib

from app.models.schemas import TextRequest, ProcessResult, AsyncTaskResponse
from app.models.database import get_db, ProcessingHistory
from app.services.ai_processor import ai_processor
from app.services.celery_app import long_text_processing

router = APIRouter()

@router.get("/")
async def root():
    return {"message": "AI学术润色系统 API v1"}

@router.post("/process", response_model=ProcessResult)
async def process_text(
    request: TextRequest, 
    db: Session = Depends(get_db)
):
    """同步文本处理接口"""
    try:
        # 处理文本
        result = await ai_processor.process_text(request.content, request.style)
        
        # 保存处理历史
        db_history = ProcessingHistory(
            user_id="anonymous",  # 实际项目中从JWT token获取
            original_text=request.content,
            processed_text=result["text"],
            ai_probability=result["ai_score"],
            processing_time=result["processing_time"]
        )
        db.add(db_history)
        db.commit()
        
        return ProcessResult(
            original_text=request.content,
            processed_text=result["text"],
            ai_probability=result["ai_score"],
            processing_time=result["processing_time"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@router.post("/process/async", response_model=AsyncTaskResponse)
async def async_process_text(
    request: TextRequest,
    background_tasks: BackgroundTasks
):
    """异步文本处理接口"""
    try:
        # 生成任务ID
        task_id = hashlib.md5(
            f"{request.content}_{request.style}".encode()
        ).hexdigest()
        
        # 提交Celery任务
        task = long_text_processing.delay(
            request.content, 
            "anonymous",  # 实际项目中从JWT token获取
            request.style
        )
        
        return AsyncTaskResponse(
            task_id=task.id,
            status="processing",
            message="任务已提交，请稍后查询结果"
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"任务提交失败: {str(e)}")

@router.get("/task/{task_id}")
async def get_task_status(task_id: str):
    """查询异步任务状态"""
    try:
        task = long_text_processing.AsyncResult(task_id)
        
        if task.state == 'PENDING':
            return {"task_id": task_id, "status": "pending", "message": "任务等待中"}
        elif task.state == 'SUCCESS':
            return {
                "task_id": task_id, 
                "status": "completed", 
                "result": task.result
            }
        elif task.state == 'FAILURE':
            return {
                "task_id": task_id, 
                "status": "failed", 
                "error": str(task.info)
            }
        else:
            return {"task_id": task_id, "status": task.state}
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"查询失败: {str(e)}")

@router.get("/health")
async def health_check():
    """健康检查接口"""
    return {
        "status": "healthy",
        "service": "AI学术润色系统",
        "version": "1.0.0"
    }
