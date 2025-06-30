# 快速检查项目状态
echo "=== 当前项目状态 ==="
echo "目录: $(pwd)"
echo "虚拟环境: $(which python)"
echo ""
echo "=== 主要文件 ==="
ls -la *.py *.txt *.md *.env 2>/dev/null
echo ""
echo "=== app目录 ==="
find app -name "*.py" | head -10
echo ""
echo "=== 服务检查 ==="
curl -s http://localhost:8000/api/v1/health 2>/dev/null || echo "服务未运行"