from rich.panel import Panel
from rich.text import Text
from chat_cli.core.types import Message, MessageType, UserMessage, SystemMessage, ErrorMessage
from chat_cli.core.constants import UIConstants

class MessageRenderer:
    @staticmethod
    def render(message: Message) -> Text | str:
        if isinstance(message, SystemMessage) or message.type == MessageType.SYSTEM:
            return f"[system]{UIConstants.SYSTEM_NAME}:[/system] {message.content}"
        
        elif isinstance(message, ErrorMessage) or message.type == MessageType.ERROR:
            return f"[error]{UIConstants.ERROR_NAME}:[/error] {message.content}"
        
        elif isinstance(message, UserMessage) or message.type == MessageType.USER:
            style = "user.self" if message.sender == "You" else "user.other"
            return f"[{style}]{message.sender}:[/{style}] {message.content}"
        
        return str(message.content)

class WelcomeRenderer:
    @staticmethod
    def render() -> Panel:
        return Panel.fit(
            f"[welcome]{UIConstants.WELCOME_TEXT}[/welcome]",
            border_style=UIConstants.WELCOME_BORDER
        )
