from celery import Celery
from app.core.config import settings

# Celery配置
celery_app = Celery(
    "ai_processor",
    broker=settings.redis_url,
    backend=settings.redis_url,
    include=['app.services.celery_app']
)

# Celery配置
celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
    task_routes={
        'app.services.celery_app.long_text_processing': 'long-running',
    }
)

@celery_app.task
def long_text_processing(text: str, user_id: str, style: str = "academic"):
    """长文本处理异步任务"""
    from app.services.ai_processor import ai_processor
    import asyncio
    
    # 在Celery任务中运行异步函数
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    
    try:
        result = loop.run_until_complete(
            ai_processor.process_text(text, style)
        )
        return {
            "user_id": user_id,
            "status": "completed",
            "result": result
        }
    except Exception as e:
        return {
            "user_id": user_id,
            "status": "failed",
            "error": str(e)
        }
    finally:
        loop.close()
