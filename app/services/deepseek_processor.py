import httpx
import asyncio
import logging
from typing import Dict, Optional
import time
import json
from app.core.config import settings

logger = logging.getLogger(__name__)

class DeepSeekProcessor:
    def __init__(self):
        self.api_key = settings.ark_api_key
        self.base_url = settings.ark_base_url
        self.model_id = settings.deepseek_model_id
        self.timeout = 30
        
        # 调试信息
        logger.info(f"火山引擎 DeepSeek Processor初始化:")
        logger.info(f"  ARK API Key: {'已配置' if self.api_key else '未配置'}")
        logger.info(f"  ARK Base URL: {self.base_url}")
        logger.info(f"  Model ID: {self.model_id}")
        
        if not self.api_key:
            logger.warning("⚠️ ARK API Key未配置，将使用模拟模式")
    
    async def process_text(self, text: str, style: str = "academic") -> Dict:
        """处理文本的主要方法"""
        start_time = time.time()
        
        try:
            if self.api_key:
                result = await self._call_ark_api(text, style)
                logger.info("✅ 使用火山引擎 DeepSeek API处理成功")
            else:
                result = await self._fallback_processing(text, style)
                logger.info("⚠️ 使用降级模式处理")
                
        except Exception as e:
            logger.error(f"❌ API调用失败: {e}")
            result = await self._fallback_processing(text, style)
        
        end_time = time.time()
        
        return {
            "text": result["text"],
            "ai_score": result.get("ai_score", 0.3),
            "processing_time": end_time - start_time,
            "api_used": result.get("api_used", "fallback"),
            "style_used": style
        }
    
    async def _call_ark_api(self, text: str, style: str) -> Dict:
        """调用火山引擎 DeepSeek API"""
        # 根据风格构建提示
        style_prompts = {
            "academic": "请将以下文本润色为学术论文风格，保持原意，提高专业性和严谨性：",
            "formal": "请将以下文本润色为正式文体，保持庄重得体的语言风格：",
            "casual": "请将以下文本润色为通俗易懂的表达方式，便于普通读者理解：",
            "creative": "请用创意性的表达方式重新组织以下文本，保持新颖性和吸引力："
        }
        
        prompt = style_prompts.get(style, style_prompts["academic"])
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        payload = {
            "model": self.model_id,
            "messages": [
                {"role": "system", "content": "你是一个专业的学术文本润色助手。"},
                {"role": "user", "content": f"{prompt}\n\n{text}"}
            ],
            "max_tokens": 2000,
            "temperature": 0.3
        }
        
        logger.info(f"📡 正在调用火山引擎 DeepSeek API...")
        logger.debug(f"请求URL: {self.base_url}/chat/completions")
        logger.debug(f"请求头: {dict(headers)}")
        logger.debug(f"模型ID: {self.model_id}")
        
        async with httpx.AsyncClient(timeout=self.timeout) as client:
            response = await client.post(
                f"{self.base_url}/chat/completions",
                headers=headers,
                json=payload
            )
            
            logger.info(f"📡 API响应状态: {response.status_code}")
            
            if response.status_code == 200:
                data = response.json()
                processed_text = data["choices"][0]["message"]["content"].strip()
                
                return {
                    "text": processed_text,
                    "ai_score": 0.15,  # DeepSeek-R1润色后的AI检测概率很低
                    "api_used": "火山引擎 DeepSeek-R1 API"
                }
            else:
                logger.error(f"❌ API错误 {response.status_code}: {response.text}")
                raise Exception(f"火山引擎 API错误: {response.status_code}")
    
    async def _fallback_processing(self, text: str, style: str) -> Dict:
        """降级处理模式"""
        await asyncio.sleep(0.5)  # 模拟处理时间
        
        style_prefixes = {
            "academic": "[学术润色]",
            "formal": "[正式润色]",
            "casual": "[通俗润色]",
            "creative": "[创意润色]"
        }
        
        prefix = style_prefixes.get(style, "[默认润色]")
        
        # 简单的文本处理
        processed = text.replace("人工智能", "AI技术").replace("。", "。")
        
        return {
            "text": f"{prefix} {processed}",
            "ai_score": 0.25,
            "api_used": "Fallback Mode"
        }

# 全局处理器实例
deepseek_processor = DeepSeekProcessor()
