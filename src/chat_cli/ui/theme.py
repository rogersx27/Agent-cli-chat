from rich.theme import Theme
from rich.style import Style
from chat_cli.core.constants import UIConstants

class ChatTheme:
    @staticmethod
    def get_theme() -> Theme:
        return Theme({
            "system": UIConstants.COLOR_SYSTEM,
            "error": UIConstants.COLOR_ERROR,
            "user.self": f"bold {UIConstants.COLOR_USER_SELF}",
            "user.other": f"bold {UIConstants.COLOR_USER_OTHER}",
            "welcome": UIConstants.COLOR_WELCOME,
        })
