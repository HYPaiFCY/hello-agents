import os
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()

# 打印配置信息（调试用）
print("=== 环境变量检查 ===")
print(f"EMBED_MODEL_TYPE: {os.getenv('EMBED_MODEL_TYPE')}")
print(f"EMBED_MODEL_NAME: {os.getenv('EMBED_MODEL_NAME')}")
print(
    f"EMBED_API_KEY: {os.getenv('EMBED_API_KEY')[:20]}..."
    if os.getenv("EMBED_API_KEY")
    else "未设置"
)
print(f"EMBED_BASE_URL: {os.getenv('EMBED_BASE_URL')}")
print()

# 测试 DashScope REST API
print("=== 测试 DashScope API ===")
try:
    import requests

    api_key = os.getenv("EMBED_API_KEY")
    base_url = os.getenv("EMBED_BASE_URL")
    model_name = os.getenv("EMBED_MODEL_NAME", "text-embedding-v3").strip('"')

    url = base_url.rstrip("/") + "/embeddings"
    headers = {"Authorization": f"Bearer {api_key}", "Content-Type": "application/json"}
    payload = {"model": model_name, "input": ["测试文本"]}

    print(f"请求URL: {url}")
    print(f"使用模型: {model_name}")

    response = requests.post(url, headers=headers, json=payload, timeout=30)

    print(f"响应状态码: {response.status_code}")

    if response.status_code == 200:
        data = response.json()
        print("✅ API调用成功!")
        print(f"嵌入维度: {len(data['data'][0]['embedding'])}")
    else:
        print(f"❌ API调用失败: {response.text}")

except Exception as e:
    print(f"❌ 测试失败: {type(e).__name__}: {e}")
    import traceback

    traceback.print_exc()
