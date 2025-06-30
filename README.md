# AI学术润色系统

> 为学生提供AI写作润色、查重检测和降重处理的一体化解决方案

## 📋 项目概述

本项目旨在解决国内学生使用AI写作但担心AI查重的矛盾需求，提供：
- **AI文本润色** - 支持学术、正式、通俗、创意等多种风格
- **AI检测功能** - 检测文本的AI生成概率
- **安全可靠** - API密钥安全管理，支持多种AI服务商

## 🚀 技术栈

### 后端框架
- **FastAPI** 0.104.1 - 现代、快速的Python Web框架
- **Uvicorn** 0.24.0 - ASGI服务器
- **SQLAlchemy** 2.0.23 - ORM数据库工具
- **Pydantic** - 数据验证和设置管理

### AI服务
- **DeepSeek API** - 主要AI文本处理服务
- **自研检测算法** - AI生成文本检测

### 开发工具
- **Python** 3.13+ - 编程语言
- **httpx** - 异步HTTP客户端
- **python-dotenv** - 环境变量管理

## 📁 项目结构

```
1AI-polish/
├── app/                        # 主应用目录
│   ├── __init__.py
│   ├── main.py                 # 原始主应用（有SQLAlchemy依赖问题）
│   ├── main_simple.py          # 简化版本（无数据库）
│   ├── main_deepseek.py        # DeepSeek API集成版本（推荐）
│   ├── api/                    # API路由模块
│   │   ├── __init__.py
│   │   ├── dependencies/
│   │   │   └── __init__.py
│   │   └── v1/
│   │       ├── __init__.py
│   │       └── endpoints.py    # API端点定义
│   ├── core/                   # 核心配置模块
│   │   ├── __init__.py
│   │   └── config.py           # 应用配置
│   ├── models/                 # 数据模型
│   │   ├── __init__.py
│   │   ├── database.py         # 数据库模型
│   │   └── schemas.py          # Pydantic模型
│   ├── services/               # 业务逻辑服务
│   │   ├── __init__.py
│   │   ├── ai_processor.py     # AI处理服务
│   │   └── celery_app.py       # 异步任务配置
│   └── utils/                  # 工具模块
│       └── __init__.py
├── tests/                      # 测试目录
│   ├── __init__.py
│   └── test_api.py             # API测试
├── config/                     # 配置文件目录
├── logs/                       # 日志目录
├── fastapi_env/               # Python虚拟环境
├── requirements.txt           # Python依赖
├── .env                       # 环境变量（敏感信息）
├── .gitignore                # Git忽略文件
└── README.md                 # 项目文档
```

## ⚙️ 环境配置

### Python环境
- **Python版本**: 3.13.5
- **虚拟环境**: `fastapi_env`
- **包管理**: pip

### 已安装的包
```
fastapi==0.104.1
uvicorn==0.24.0
sqlalchemy==2.0.23
python-dotenv==1.0.0
typing-extensions>=4.0.0
pydantic-settings==2.10.1
httpx (最新版本)
```

### 环境变量 (.env)
```bash
# 应用配置
APP_NAME="AI学术润色系统"
DEBUG=True
SECRET_KEY="your-secret-key-here-change-in-production"

# 数据库配置
DATABASE_URL="sqlite:///./ai_processor.db"

# Redis配置
REDIS_URL="redis://localhost:6379"

# AI服务配置
DEEPSEEK_API_KEY=your_deepseek_api_key_here
DEEPSEEK_BASE_URL=https://api.deepseek.com/v1
```

## 🛠️ 安装与运行

### 1. 环境准备
```bash
# 克隆项目
cd 1AI-polish

# 激活虚拟环境
source fastapi_env/bin/activate  # macOS/Linux

# 安装依赖
pip install -r requirements.txt
```

### 2. 配置API密钥
```bash
# 编辑环境变量文件
nano .env

# 替换为您的实际DeepSeek API密钥
DEEPSEEK_API_KEY=sk-your-actual-api-key-here
```

### 3. 启动服务
```bash
# 方式1：使用DeepSeek集成版本（推荐）
uvicorn app.main_deepseek:app --reload --host 0.0.0.0 --port 8000

# 方式2：使用简化版本（测试用）
uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000
```

### 4. 访问服务
- **主页**: http://localhost:8000
- **API文档**: http://localhost:8000/docs
- **替代文档**: http://localhost:8000/redoc

## 🔧 API接口

### 核心接口

#### 1. 文本润色 `POST /api/v1/process`
```json
{
  "content": "人工智能技术在学术写作中的应用越来越广泛",
  "style": "academic"
}
```

**响应**:
```json
{
  "original_text": "人工智能技术在学术写作中的应用越来越广泛",
  "processed_text": "[学术润色] AI技术在学术写作中的应用越来越广泛",
  "ai_probability": 0.25,
  "processing_time": 0.8,
  "style_used": "academic",
  "api_used": "DeepSeek API"
}
```

#### 2. AI检测 `POST /api/v1/detect`
```json
{
  "content": "要检测的文本内容"
}
```

#### 3. 获取风格列表 `GET /api/v1/styles`
返回支持的润色风格列表

#### 4. 健康检查 `GET /api/v1/health`
服务状态检查

### 支持的润色风格
- `academic` - 学术论文风格
- `formal` - 正式文体风格  
- `casual` - 通俗易懂风格
- `creative` - 创意表达风格

## 🎯 核心功能

### 1. AI文本润色
- 集成DeepSeek API进行高质量文本润色
- 支持多种写作风格转换
- 智能保持原文含义
- API故障时自动降级到备用模式

### 2. AI检测算法
- **模式匹配**: 检测AI写作常见句式
- **复杂度分析**: 分析句子长度一致性
- **结构检测**: 识别规律性写作特征
- **综合评分**: 0-1概率值 + 置信度等级

### 3. 安全特性
- 环境变量管理API密钥
- Git忽略敏感信息
- CORS跨域支持
- 错误处理和降级机制

## 🚀 开发路线图

### 已完成 ✅
- [x] FastAPI基础框架搭建
- [x] DeepSeek API集成
- [x] AI检测算法实现
- [x] 多风格润色支持
- [x] 安全的配置管理
- [x] API文档自动生成

### 进行中 🔄
- [ ] SQLAlchemy数据库集成修复
- [ ] 用户认证系统
- [ ] 处理历史记录
- [ ] 异步任务队列(Celery)

### 计划中 📋
- [ ] 前端Vue.js界面开发
- [ ] 用户注册登录功能
- [ ] 批量文本处理
- [ ] 更多AI服务商集成
- [ ] 性能优化和缓存
- [ ] 部署和监控

## 🧪 测试

### 运行测试
```bash
# 运行所有测试
pytest tests/ -v

# 测试特定文件
pytest tests/test_api.py -v
```

### 手动测试
1. 访问 http://localhost:8000/docs
2. 展开 `POST /api/v1/process` 接口
3. 点击 "Try it out"
4. 输入测试数据并执行

## 🔍 故障排除

### 常见问题

1. **端口被占用**
   ```bash
   lsof -i :8000
   kill -9 [PID]
   ```

2. **API密钥未配置**
   - 检查 `.env` 文件中的 `DEEPSEEK_API_KEY`
   - 服务会自动降级到模拟模式

3. **SQLAlchemy兼容性问题**
   - 使用 `main_deepseek.py` 替代 `main.py`
   - 或升级SQLAlchemy版本

4. **依赖安装失败**
   ```bash
   pip install --upgrade pip
   pip install -r requirements.txt --force-reinstall
   ```

## 🤝 开发团队

- **后端开发**: AI学术润色核心功能
- **前端开发**: Vue.js用户界面（计划中）
- **产品设计**: 用户体验和需求调研
- **算法优化**: AI检测算法改进

## 📝 更新日志

### v1.0.0 (当前版本)
- 初始版本发布
- DeepSeek API集成
- 基础润色和检测功能
- API文档和安全配置

## 📄 许可证

本项目为教育和研究目的开发，请遵守相关AI服务的使用条款。

## 📞 联系方式

如有问题或建议，请联系开发团队。

---

**注意**: 请确保API密钥的安全，不要将 `.env` 文件提交到代码仓库。