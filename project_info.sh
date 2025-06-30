#!/bin/bash
echo "======================================"
echo "AI学术润色系统 - 项目信息报告"
echo "======================================"
echo "生成时间: $(date)"
echo ""

echo "=== 1. 系统环境 ==="
echo "操作系统: $(uname -s)"
echo "Python版本: $(python --version)"
echo "当前目录: $(pwd)"
echo "虚拟环境: $VIRTUAL_ENV"
echo ""

echo "=== 2. 项目文件结构 ==="
if command -v tree &> /dev/null; then
    tree -a -I 'fastapi_env|__pycache__|*.pyc|.git'
else
    find . -type f -not -path './fastapi_env/*' -not -path './.git/*' -not -name '*.pyc' | sort
fi
echo ""

echo "=== 3. 已安装的Python包 ==="
pip list | head -20
echo ""

echo "=== 4. 环境变量配置 ==="
echo "APP_NAME: ${APP_NAME:-未设置}"
echo "DEBUG: ${DEBUG:-未设置}"
echo "DEEPSEEK_API_KEY: ${DEEPSEEK_API_KEY:+已配置}"
echo "DATABASE_URL: ${DATABASE_URL:-未设置}"
echo ""

echo "=== 5. 主要配置文件 ==="
echo "--- requirements.txt ---"
cat requirements.txt 2>/dev/null || echo "文件不存在"
echo ""
echo "--- .env 示例（隐藏敏感信息）---"
cat .env 2>/dev/null | sed 's/=.*/=***/' || echo "文件不存在"
echo ""

echo "=== 6. Git状态 ==="
git status --porcelain 2>/dev/null || echo "不是Git仓库"
echo ""

echo "=== 7. 服务状态检查 ==="
echo "检查端口8000占用情况:"
lsof -i :8000 2>/dev/null || echo "端口8000空闲"
echo ""

echo "=== 8. 可执行的启动命令 ==="
echo "uvicorn app.main_deepseek:app --reload --host 0.0.0.0 --port 8000"
echo "uvicorn app.main_simple:app --reload --host 0.0.0.0 --port 8000"
echo ""

echo "=== 9. 重要链接 ==="
echo "主页: http://localhost:8000"
echo "API文档: http://localhost:8000/docs"
echo "健康检查: http://localhost:8000/api/v1/health"
echo ""
echo "======================================"
