from datetime import datetime
from enum import Enum
from typing import Literal, Union
from pydantic import BaseModel, Field

class MessageType(str, Enum):
    SYSTEM = "SYSTEM"
    USER = "USER"
    ERROR = "ERROR"

class BaseMessage(BaseModel):
    type: MessageType
    content: str
    sender: str
    timestamp: datetime = Field(default_factory=datetime.now)

class UserMessage(BaseMessage):
    type: Literal[MessageType.USER] = MessageType.USER

class SystemMessage(BaseMessage):
    type: Literal[MessageType.SYSTEM] = MessageType.SYSTEM
    sender: str = "System"

class ErrorMessage(BaseMessage):
    type: Literal[MessageType.ERROR] = MessageType.ERROR
    sender: str = "Error"

Message = Union[UserMessage, SystemMessage, ErrorMessage]
