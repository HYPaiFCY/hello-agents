from typing import Any, Dict, List
from hello_agents import HelloAgentsLLM, ReflectionAgent


# --- 模块 1: 记忆模块 ---
class Memory:
    """
    一个简单的短期记忆模块，用于存储智能体的行动与反思轨迹
    """

    def __init__(self):
        self.records: List[Dict[str, Any]] = []

    def add_record(self, record_type: str, content: str):
        """
        向记忆存储模块中添加记录。

        参数：
        - record_type(str):记录的类型("execution"或"reflection")
        - content(str):记录的具体内容(例如生成的内容或反思的反馈)
        """
        self.records.append({"type": record_type, "content": content})
        print(f"📝 记忆已更新，新增一条 '{record_type}' 记录。")

    def get_trajectory(self) -> str:
        """
        将记忆模块中的记录格式化为一个连串的字符串文本，用于构建prompt"""
        trajectory = ""
        for record in self.records:
            if record["type"] == "execution":
                trajectory += f"---上一轮尝试---\n{record['content']}\n\n"
            elif record["type"] == "reflection":
                trajectory += f"---评审员反馈---\n{record['content']}\n\n"
        return trajectory.strip()

    def get_last_execution(self) -> str:
        """
        获取最近一次的执行结果
        """
        for record in reversed(self.records):
            if record["type"] == "execution":
                return record["content"]
        return None


# --- 模块 2: Reflection 智能体 ---
# 默认提示词模板
DEFAULT_PROMPTS = {
    "initial": """
请根据以下要求完成任务:

任务: {task}

请提供一个完整、准确的回答。
""",
    "reflect": """
请仔细审查以下回答，并找出可能的问题或改进空间:

# 原始任务:
{task}

# 当前回答:
{content}

请分析这个回答的质量，指出不足之处，并提出具体的改进建议。
如果回答已经很好，请回答"无需改进"。
""",
    "refine": """
请根据反馈意见改进你的回答:

# 原始任务:
{task}

# 上一轮回答:
{last_attempt}

# 反馈意见:
{feedback}

请提供一个改进后的回答。
""",
}


class MyReflectionAgent:
    """
    继承HelloAgentsLLM的Reflection智能体类
    """

    def __init__(
        self,
        llm: HelloAgentsLLM,
        name: str,
        custom_prompts: Dict[str, str] = None,
        max_iterations: int = 3,
    ):
        self.llm = llm
        self.name = name
        self.memory = Memory()
        self.prompts = custom_prompts if custom_prompts else DEFAULT_PROMPTS
        self.max_iterations = max_iterations
        print(f"✅ {name} 初始化完成。")

    def run(self, task: str) -> str:
        """
        执行反思任务的主方法

        参数:
        - task(str): 需要完成的任务描述

        返回:
        - 最终生成的结果字符串
        """
        print(f"🚀 {self.name} 开始处理任务: {task}")

        # 初始执行阶段
        initial_prompt = self.prompts["initial"].format(task=task)
        initial_response = self._get_llm_response(initial_prompt)
        self.memory.add_record("execution", initial_response)
        print(f"初始回答:\n{initial_response}\n")

        for iteration in range(self.max_iterations):
            print(f"🔄 迭代第 {iteration + 1} 轮反思与优化")

            # 反思阶段
            last_execution = self.memory.get_last_execution()
            reflect_prompt = self.prompts["reflect"].format(
                task=task, content=last_execution
            )
            reflection_feedback = self._get_llm_response(reflect_prompt)
            self.memory.add_record("reflection", reflection_feedback)
            print(f"评审员反馈:\n{reflection_feedback}\n")

            if "无需改进" in reflection_feedback:
                print("✅ 评审员认为当前回答已足够好，结束迭代。")
                break

            # 优化阶段
            refine_prompt = self.prompts["refine"].format(
                task=task, last_attempt=last_execution, feedback=reflection_feedback
            )
            refined_response = self._get_llm_response(refine_prompt)
            self.memory.add_record("execution", refined_response)
            print(f"优化后的回答:\n{refined_response}\n")

        final_result = self.memory.get_last_execution()
        print(f"🎉 {self.name} 完成任务，最终结果:\n{final_result}")
        return final_result

    def _get_llm_response(self, prompt: str, **kwargs) -> str:
        """调用LLM并获取完整响应"""
        messages = [{"role": "user", "content": prompt}]
        return self.llm.invoke(messages, **kwargs) or ""
