from pydantic_settings import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

# 确保加载环境变量
load_dotenv()

class Settings(BaseSettings):
    app_name: str = "AI学术润色系统"
    debug: bool = True
    secret_key: str = "your-secret-key-here"
    
    # 数据库配置
    database_url: str = "sqlite:///./ai_processor.db"
    
    # Redis配置
    redis_url: str = "redis://localhost:6379"
    
    # 火山引擎 DeepSeek API 配置
    ark_api_key: Optional[str] = None
    ark_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    deepseek_model_id: str = "deepseek-r1-250528"
    
    # 兼容旧配置
    openai_api_key: Optional[str] = None
    deepseek_api_key: Optional[str] = None  # 兼容性
    deepseek_base_url: str = "https://ark.cn-beijing.volces.com/api/v3"
    
    # 性能配置
    max_text_length: int = 10000
    request_timeout: int = 30
    
    class Config:
        env_file = ".env"
        case_sensitive = False

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 手动检查环境变量
        if not self.ark_api_key:
            self.ark_api_key = os.getenv('ARK_API_KEY')
        if not self.ark_base_url:
            self.ark_base_url = os.getenv('ARK_BASE_URL', 'https://ark.cn-beijing.volces.com/api/v3')
        if not self.deepseek_model_id:
            self.deepseek_model_id = os.getenv('DEEPSEEK_MODEL_ID', 'deepseek-r1-250528')

# 创建全局设置实例
settings = Settings()

# 调试输出
if settings.debug:
    print(f"DEBUG: ARK API Key loaded: {'Yes' if settings.ark_api_key else 'No'}")
    print(f"DEBUG: ARK Base URL: {settings.ark_base_url}")
    print(f"DEBUG: DeepSeek Model ID: {settings.deepseek_model_id}")
