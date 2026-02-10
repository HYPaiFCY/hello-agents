from dotenv import load_dotenv

load_dotenv()
from hello_agents import SimpleAgent, HelloAgentsLLM, ToolRegistry
from hello_agents.tools import MemoryTool

memory_tool = MemoryTool(user_id="user123")
tool_registry = ToolRegistry()
tool_registry.register_tool(memory_tool)
# agent.tool_registry = tool_registry
# 基础搜索
result = memory_tool.execute("search", query="Python编程", limit=5)
print(f"\n搜索关于“Python编程”的结果: {result}\n")
# 指定记忆类型搜索
result = memory_tool.execute(
    "search", query="学习进度", memory_type="episodic", limit=3
)
print(f"\n搜索关于“学习进度”的结果: {result}\n")
# 多类型搜索
result = memory_tool.execute(
    "search",
    query="函数定义",
    memory_types=["semantic", "episodic"],
    min_importance=0.5,
)
print(f"\n搜索关于“函数定义”的结果: {result}\n")
