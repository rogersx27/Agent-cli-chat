from enum import Enum

class Commands(str, Enum):
    QUIT = "/quit"

class UIConstants:
    PROMPT = "You: "
    SYSTEM_NAME = "System"
    ERROR_NAME = "Error"
    
    # Colors (Rich style strings)
    COLOR_SYSTEM = "bold yellow"
    COLOR_ERROR = "bold red"
    COLOR_USER_SELF = "green"
    COLOR_USER_OTHER = "blue"
    COLOR_WELCOME = "bold magenta"
    
    WELCOME_TEXT = "Welcome to CLI Chat!"
    WELCOME_BORDER = "magenta"

class ProtocolConstants:
    ENCODING = "utf-8"
    HEADER_FORMAT = ">I"
    HEADER_SIZE = 4
