import ast
from hello_agents import HelloAgentsLLM
from typing import Optional, List, Dict, Any

# 默认规划器提示词模板
DEFAULT_PLANNER_PROMPT = """
你是一个顶级的AI规划专家。你的任务是将用户提出的复杂问题分解成一个由多个简单步骤组成的行动计划。
请确保计划中的每个步骤都是一个独立的、可执行的子任务，并且严格按照逻辑顺序排列。
你的输出必须是一个Python列表，其中每个元素都是一个描述子任务的字符串。

问题: {question}

请严格按照以下格式输出你的计划:
```python
["步骤1", "步骤2", "步骤3", ...]
```
"""

# 默认执行器提示词模板
DEFAULT_EXECUTOR_PROMPT = """
你是一位顶级的AI执行专家。你的任务是严格按照给定的计划，一步步地解决问题。
你将收到原始问题、完整的计划、以及到目前为止已经完成的步骤和结果。
请你专注于解决"当前步骤"，并仅输出该步骤的最终答案，不要输出任何额外的解释或对话。

# 原始问题:
{question}

# 完整计划:
{plan}

# 历史步骤与结果:
{history}

# 当前步骤:
{current_step}

请仅输出针对"当前步骤"的回答:
"""


class Planner:
    """
    规划器-负责将复杂问题分解为简单步骤
    """

    def __init__(
        self, llm_client: HelloAgentsLLM, prompt_template: str = DEFAULT_PLANNER_PROMPT
    ):
        self.llm_client = llm_client
        self.prompt_template = (
            prompt_template["planner"] if prompt_template else DEFAULT_PLANNER_PROMPT
        )

    def plan(self, question: str, **kwargs) -> list[str]:
        """
        生成执行计划
        """
        prompt = self.prompt_template.format(question=question)
        messages = [{"role": "user", "content": prompt}]

        print("---正在生成计划---")
        reponse_text = self.llm_client.invoke(messages=messages, **kwargs) or ""
        print(f"✅ 计划已生成:\n{reponse_text}")

        try:
            plan_str = reponse_text.split("```python")[1].split("```")[0].strip()
            plan = ast.literal_eval(plan_str)
            return plan if isinstance(plan, list) else []
        except (ValueError, SyntaxError, IndexError) as e:
            print(f"❌ 解析计划时出错: {e}")
            print(f"原始响应: {reponse_text}")
            return []
        except Exception as e:
            print(f"❌ 解析计划时发生未知错误: {e}")
            return []


class Executor:
    """执行器-负责执行步骤"""

    def __init__(
        self,
        llm_client: HelloAgentsLLM,
        prompt_template: str = DEFAULT_EXECUTOR_PROMPT,
    ):
        self.llm_client = llm_client
        self.prompt_template = (
            prompt_template["executor"] if prompt_template else DEFAULT_EXECUTOR_PROMPT
        )

    def execute(self, question: str, plan: list[str], **kwargs) -> str:
        history = ""
        final_answer = ""

        print("\n---正在执行计划---")
        for i, step in enumerate(plan, 1):
            print(f"\n-> 正在执行步骤{i}/{len(plan)}: {step}")
            prompt = self.prompt_template.format(
                question=question,
                plan=plan,
                history=history if history else "无",
                current_step=step,
            )

            response_text = (
                self.llm_client.invoke(
                    messages=[{"role": "user", "content": prompt}], **kwargs
                )
                or ""
            )
            history += f"\n步骤 {i}: {step}\n结果: {response_text}\n"
            print(f"✅ 步骤{i}已完成，结果:\n{response_text}")
            final_answer = response_text
        return final_answer


class MyPlanAndSolveAgent:
    """规划与执行代理 - 结合规划器和执行器"""

    def __init__(
        self,
        name: str,
        llm_client: HelloAgentsLLM,
        prompt_template: Optional[dict[str, str]] = None,
    ):
        self.name = name
        self.llm_client = llm_client
        self.planner = Planner(llm_client, prompt_template)
        self.executor = Executor(llm_client, prompt_template)

    def run(self, question: str, **kwargs) -> str:
        plan = Planner.plan(self.planner, question, **kwargs)
        if not plan:
            print("❌ 未能生成有效的计划，无法继续执行。")
            return "无法生成计划。"
        final_answer = Executor.execute(self.executor, question, plan, **kwargs)

        return final_answer
