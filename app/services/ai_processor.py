import asyncio
from typing import Dict, Optional
import time
import random

class AIProcessor:
    def __init__(self):
        self.processing_delay = 0.5  # 模拟处理时间
    
    async def process_text(self, text: str, style: str = "academic") -> Dict:
        """AI文本处理主函数"""
        start_time = time.time()
        
        # 模拟异步AI处理
        await asyncio.sleep(self.processing_delay)
        
        # 模拟不同风格的处理结果
        processed_text = await self._apply_style(text, style)
        ai_score = await self._calculate_ai_probability(processed_text)
        
        end_time = time.time()
        
        return {
            "text": processed_text,
            "ai_score": ai_score,
            "processing_time": end_time - start_time
        }
    
    async def _apply_style(self, text: str, style: str) -> str:
        """根据风格调整文本"""
        style_prefixes = {
            "academic": "[学术润色]",
            "formal": "[正式润色]", 
            "casual": "[通俗润色]",
            "creative": "[创意润色]"
        }
        
        prefix = style_prefixes.get(style, "[默认润色]")
        
        # 模拟文本处理逻辑
        if "人工智能" in text:
            processed = text.replace("人工智能", "AI技术")
        else:
            processed = text
            
        return f"{prefix} {processed}"
    
    async def _calculate_ai_probability(self, text: str) -> float:
        """计算AI生成概率"""
        # 简单的AI检测逻辑模拟
        ai_indicators = ["首先", "其次", "最后", "综上所述", "总而言之"]
        score = 0.0
        
        for indicator in ai_indicators:
            if indicator in text:
                score += 0.1
        
        # 添加随机因素模拟真实检测结果
        score += random.uniform(0.1, 0.3)
        
        return min(score, 1.0)

# 全局AI处理器实例
ai_processor = AIProcessor()
