from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    app_name: str = "AI学术润色系统"
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    
    # 数据库配置
    database_url: str = "sqlite:///./ai_processor.db"
    
    # Redis配置
    redis_url: str = "redis://localhost:6379"
    
    # AI服务配置
    openai_api_key: Optional[str] = None
    
    # 性能配置
    max_text_length: int = 10000
    request_timeout: int = 30
    
    model_config = {
        "env_file": ".env",
        "extra": "ignore"  # 忽略额外的环境变量
    }

settings = Settings()
