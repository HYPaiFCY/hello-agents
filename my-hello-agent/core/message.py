from typing import Optional, Dict, Any, Literal
from datetime import datetime
from pydantic import BaseModel

MessageRole =Literal["user","assistant","system","tool"]

class Message(BaseModel):
    """
    消息类，表示对话中的一条消息。
    """
    content: str
    role: MessageRole
    timestamp: datetime = None
    metadata: Optional[Dict[str,Any]] = None
    
    
    def __init__(self,content:str,role:MessageRole,**kwargs):
        super().__init__(
            content=content,
            role=role,
            timestamp=kwargs.get("timestamp",datetime.now()),
            metadata=kwargs.get("metadata",{})
        )
        
    def to_dict(self) ->Dict[str,Any]:
        """
        将消息转换为字典格式，适用于LLM调用。
        """
        return {
            "role":self.role,
            "content":self.content
        }
        
    def __str__(self) -> str:
        return f"[{self.timestamp}] {self.role.upper()}: {self.content}"