from qdrant_client import QdrantClient
from dotenv import load_dotenv
import os

load_dotenv()

client = QdrantClient(url=os.getenv("QDRANT_URL"), api_key=os.getenv("QDRANT_API_KEY"))

# 列出所有集合
collections = client.get_collections()
print("现有集合:")
for col in collections.collections:
    info = client.get_collection(col.name)
    print(
        f"  - {col.name}: {info.vectors_count} vectors, dim={info.config.params.vectors.size}"
    )
    client.delete_collection(col.name)
    # print(f"    已删除集合: {col.name}")

# 删除指定集合
# try:
#     client.delete_collection("rag_knowledge_base")
#     print("✅ 成功删除 rag_knowledge_base 集合")
# except Exception as e:
#     print(f"❌ 删除失败: {e}")
