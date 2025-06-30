# app/main_deepseek.py - 安全的 DeepSeek API 集成版本
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Optional
import asyncio
import time
import httpx
import json
import random
import re
import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 从环境变量读取配置
DEEPSEEK_API_KEY = os.getenv("DEEPSEEK_API_KEY")
DEEPSEEK_BASE_URL = os.getenv("DEEPSEEK_BASE_URL", "https://api.deepseek.com/v1")

# 验证必要的环境变量
if not DEEPSEEK_API_KEY:
    print("警告: DEEPSEEK_API_KEY 未设置，将使用模拟模式")

# 创建FastAPI应用
app = FastAPI(
    title="AI学术润色系统",
    description="为学生提供AI写作润色、查重检测和降重处理服务",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 数据模型
class TextRequest(BaseModel):
    content: str = Field(..., min_length=1, max_length=10000, description="要处理的文本内容")
    style: Optional[str] = Field(default="academic", description="润色风格：academic, formal, casual, creative")

class ProcessResult(BaseModel):
    original_text: str = Field(description="原始文本")
    processed_text: str = Field(description="润色后的文本")
    ai_probability: float = Field(description="AI检测概率 (0-1)")
    processing_time: float = Field(description="处理时间（秒）")
    style_used: str = Field(description="使用的润色风格")
    api_used: str = Field(description="使用的API服务")

class AIDetectionResult(BaseModel):
    ai_probability: float = Field(description="AI生成概率")
    confidence: str = Field(description="置信度等级")
    details: dict = Field(description="检测详情")

# DeepSeek API 客户端
class DeepSeekClient:
    def __init__(self):
        self.api_key = DEEPSEEK_API_KEY
        self.base_url = DEEPSEEK_BASE_URL
        self.client = httpx.AsyncClient(timeout=30.0) if self.api_key else None
    
    async def polish_text(self, text: str, style: str) -> tuple[str, str]:
        """使用 DeepSeek API 润色文本"""
        
        # 如果没有API密钥，使用模拟模式
        if not self.api_key:
            return self._mock_polish(text, style), "模拟模式"
        
        style_prompts = {
            "academic": "请将以下文本润色为学术论文风格，保持原意，使用正式、准确的学术表达：",
            "formal": "请将以下文本润色为正式文体，语言庄重、严谨、专业：",
            "casual": "请将以下文本润色为通俗易懂的表达，语言自然流畅：", 
            "creative": "请将以下文本进行创意润色，保持原意的同时增加表达的生动性："
        }
        
        prompt = style_prompts.get(style, style_prompts["academic"])
        
        try:
            response = await self.client.post(
                f"{self.base_url}/chat/completions",
                headers={
                    "Authorization": f"Bearer {self.api_key}",
                    "Content-Type": "application/json"
                },
                json={
                    "model": "deepseek-chat",
                    "messages": [
                        {
                            "role": "system", 
                            "content": "你是一个专业的文本润色助手。请根据要求对文本进行润色，保持原意不变，只改善表达方式。直接返回润色后的文本，不要添加额外说明。"
                        },
                        {
                            "role": "user", 
                            "content": f"{prompt}\n\n{text}"
                        }
                    ],
                    "temperature": 0.3,
                    "max_tokens": 2000
                }
            )
            
            if response.status_code == 200:
                result = response.json()
                polished_text = result['choices'][0]['message']['content'].strip()
                return polished_text, "DeepSeek API"
            else:
                print(f"DeepSeek API 错误: {response.status_code}")
                return self._mock_polish(text, style), "备用模式"
                
        except Exception as e:
            print(f"DeepSeek API 调用失败: {e}")
            return self._mock_polish(text, style), "备用模式"
    
    def _mock_polish(self, text: str, style: str) -> str:
        """模拟润色（当API不可用时）"""
        style_prefixes = {
            "academic": "[学术润色]",
            "formal": "[正式润色]", 
            "casual": "[通俗润色]",
            "creative": "[创意润色]"
        }
        
        prefix = style_prefixes.get(style, "[默认润色]")
        
        # 简单的文本替换示例
        processed = text.replace("人工智能", "AI技术")
        processed = processed.replace("机器学习", "ML技术")
        
        return f"{prefix} {processed}"

# AI检测器
class AIDetector:
    def __init__(self):
        # AI写作常见特征模式
        self.ai_patterns = [
            r'首先.*其次.*最后',
            r'综上所述',
            r'总而言之',
            r'总的来说',
            r'一方面.*另一方面',
            r'不仅.*而且',
            r'值得注意的是',
            r'需要指出的是'
        ]
    
    def detect_ai_probability(self, text: str) -> dict:
        """检测文本的AI生成概率"""
        scores = []
        
        # 1. 模式匹配检测
        pattern_score = self._pattern_analysis(text)
        scores.append(pattern_score)
        
        # 2. 语言复杂度分析
        complexity_score = self._complexity_analysis(text)
        scores.append(complexity_score)
        
        # 3. 结构规律性检测
        structure_score = self._structure_analysis(text)
        scores.append(structure_score)
        
        # 计算综合分数
        final_score = sum(scores) / len(scores)
        final_score = min(max(final_score, 0.0), 1.0)  # 限制在0-1范围
        
        # 确定置信度等级
        if final_score < 0.3:
            confidence = "低"
        elif final_score < 0.6:
            confidence = "中"
        else:
            confidence = "高"
        
        return {
            "ai_probability": final_score,
            "confidence": confidence,
            "details": {
                "pattern_score": pattern_score,
                "complexity_score": complexity_score,
                "structure_score": structure_score
            }
        }
    
    def _pattern_analysis(self, text: str) -> float:
        """AI常用模式分析"""
        matches = 0
        for pattern in self.ai_patterns:
            if re.search(pattern, text):
                matches += 1
        
        return min(matches / 3, 1.0)  # 归一化到0-1
    
    def _complexity_analysis(self, text: str) -> float:
        """语言复杂度分析"""
        sentences = re.split(r'[。！？]', text)
        sentences = [s.strip() for s in sentences if s.strip()]
        
        if not sentences:
            return 0.0
        
        # 句子长度一致性（AI倾向于生成长度相似的句子）
        lengths = [len(s) for s in sentences]
        avg_length = sum(lengths) / len(lengths)
        
        # 计算长度变异系数
        if avg_length > 0:
            variance = sum((l - avg_length) ** 2 for l in lengths) / len(lengths)
            std_dev = variance ** 0.5
            cv = std_dev / avg_length  # 变异系数
            
            # 变异系数越小，越可能是AI生成
            return max(0, 1 - cv * 2)
        
        return 0.0
    
    def _structure_analysis(self, text: str) -> float:
        """结构规律性分析"""
        # 检查是否有明显的结构化特征
        structure_indicators = [
            r'\d+\.',  # 数字列表
            r'第[一二三四五六七八九十]+',  # 中文序号
            r'[（(]\d+[）)]',  # 括号数字
        ]
        
        matches = 0
        for indicator in structure_indicators:
            if re.search(indicator, text):
                matches += 1
        
        return min(matches / 2, 1.0)

# 初始化组件
deepseek_client = DeepSeekClient()
ai_detector = AIDetector()

# API路由
@app.get("/")
async def root():
    api_status = "已配置" if DEEPSEEK_API_KEY else "未配置（模拟模式）"
    return {
        "message": "欢迎使用AI学术润色系统",
        "features": ["文本润色", "AI检测", "多种风格支持"],
        "api_status": api_status,
        "docs": "/docs",
        "version": "1.0.0"
    }

@app.get("/api/v1/health")
async def health_check():
    return {
        "status": "healthy",
        "service": "AI学术润色系统",
        "api_provider": "DeepSeek" if DEEPSEEK_API_KEY else "模拟模式",
        "version": "1.0.0"
    }

@app.post("/api/v1/process", response_model=ProcessResult)
async def process_text(request: TextRequest):
    """文本润色处理接口"""
    start_time = time.time()
    
    try:
        # 1. 使用 DeepSeek API 润色文本
        processed_text, api_used = await deepseek_client.polish_text(request.content, request.style)
        
        # 2. 检测AI概率
        detection_result = ai_detector.detect_ai_probability(processed_text)
        
        # 3. 计算处理时间
        end_time = time.time()
        processing_time = end_time - start_time
        
        return ProcessResult(
            original_text=request.content,
            processed_text=processed_text,
            ai_probability=detection_result["ai_probability"],
            processing_time=processing_time,
            style_used=request.style,
            api_used=api_used
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"处理失败: {str(e)}")

@app.post("/api/v1/detect", response_model=AIDetectionResult)
async def detect_ai_text(request: TextRequest):
    """AI文本检测接口"""
    try:
        result = ai_detector.detect_ai_probability(request.content)
        
        return AIDetectionResult(
            ai_probability=result["ai_probability"],
            confidence=result["confidence"],
            details=result["details"]
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"检测失败: {str(e)}")

@app.get("/api/v1/styles")
async def get_available_styles():
    """获取可用的润色风格"""
    return {
        "styles": [
            {"name": "academic", "description": "学术论文风格"},
            {"name": "formal", "description": "正式文体风格"},
            {"name": "casual", "description": "通俗易懂风格"},
            {"name": "creative", "description": "创意表达风格"}
        ]
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "main_deepseek:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
