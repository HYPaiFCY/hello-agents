"""Agent基类"""
from abc import ABC, abstractmethod
from typing import Optional, Any
from .message import Message
from .llm import HelloAgentsLLM
from .config import Config

class Agent(ABC):
    """Agent基类"""
    
    def __init__(
        self,
        name: str,
        llm: HelloAgentsLLM,
        system_prompt: Optional[str] = None,
        config: Optional[Config] = None
    ):
        self.name = name
        self.llm = llm
        self.system_prompt = system_prompt
        self.config = config or Config()
        self._history:list[Message] = []
        
    @abstractmethod
    def run(self, input_text: str, **kwargs) -> str:
        """运行Agent，处理输入并返回响应"""
        pass
    
    def add_message(self, message: Message):
        """添加消息到历史记录"""
        self._history.append(message)
        
    def clear_history(self):
        """清除历史消息"""
        self._history = []
        
    def get_history(self) -> list[Message]:
        """获取历史消息列表"""
        return self._history.copy()
    
    def __str__(self):
        return f"Agent(name={self.name}, provider={self.llm.provider})"