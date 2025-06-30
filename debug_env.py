# debug_env.py
import os
from dotenv import load_dotenv

# 显式加载.env文件
load_dotenv()

print("=== 环境变量检查 ===")
print(f"当前工作目录: {os.getcwd()}")
print(f"是否存在.env文件: {os.path.exists('.env')}")

# 检查所有环境变量
print("\n=== DeepSeek相关环境变量 ===")
deepseek_key = os.getenv('DEEPSEEK_API_KEY')
deepseek_url = os.getenv('DEEPSEEK_BASE_URL')

print(f"DEEPSEEK_API_KEY: {'已设置' if deepseek_key else '未设置'}")
print(f"DEEPSEEK_API_KEY值: {deepseek_key[:20] + '...' if deepseek_key else 'None'}")
print(f"DEEPSEEK_BASE_URL: {deepseek_url}")

# 检查OpenAI环境变量
openai_key = os.getenv('OPENAI_API_KEY')
print(f"OPENAI_API_KEY: {'已设置' if openai_key else '未设置'}")

print("\n=== 所有环境变量 ===")
for key, value in os.environ.items():
    if 'API' in key or 'DEEPSEEK' in key or 'OPENAI' in key:
        safe_value = value[:10] + '...' if value else 'None'
        print(f"{key}: {safe_value}")