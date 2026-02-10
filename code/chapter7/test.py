# from hello_agents import SimpleAgent, HelloAgentsLLM, CalculatorTool
# from dotenv import load_dotenv

# load_dotenv()

# llm=HelloAgentsLLM()

# agent=SimpleAgent(name="AI助手",
#                   llm=llm,
#                   system_prompt="你是一个有用的AI助手。")

# response=agent.run("你好，请帮我查询一下今天宣城的天气，然后根据天气推荐一个合适的旅游景点。")
# print(f"最终响应:\n{response}")


# # agent.addtool(CalculatorTool())
# # response_with_calc=agent.run("请计算一下12345乘以6789的结果是多少？")
# # print(f"带计算工具的响应:\n{response_with_calc}")
import asyncio
from hello_agents import ToolRegistry, AsyncToolExecutor
from hello_agents.tools.builtin import CalculatorTool, SearchTool
import math
from dotenv import load_dotenv

load_dotenv()


async def test_parallel_execution():
    registry = ToolRegistry()
    # registry.register_function(
    #     name="search",
    #     func=lambda query: f"搜索结果：这是关于'{query}'的一些信息.",
    #     description="根据查询关键词返回搜索结果。",
    # )

    # registry.register_function(
    #     name="my_calculator",
    #     func=lambda expression: f"计算结果：{eval(expression, {'__builtins__': None}, {'sqrt': math.sqrt})}",
    #     description="计算数学表达式的结果。",
    # )
    # 假设已经注册了搜索和计算工具
    registry.register_tool(SearchTool())
    registry.register_tool(CalculatorTool())

    executor = AsyncToolExecutor(registry)

    # 定义并行任务
    tasks = [
        {"tool_name": "search", "input_data": "Python编程"},
        {"tool_name": "search", "input_data": "机器学习"},
        {"tool_name": "python_calculator", "input_data": "2 + 2"},
        {"tool_name": f"{CalculatorTool().name}", "input_data": "sqrt(16)"},
    ]

    # 并行执行
    results = await executor.execute_tools_parallel(tasks)

    for i, result in enumerate(results):
        print(f"任务 {i+1} 结果: {result}...")


if __name__ == "__main__":
    asyncio.run(test_parallel_execution())
