from rich.console import Console
from chat_cli.core.types import Message
from chat_cli.ui.theme import ChatTheme
from chat_cli.ui.components import MessageRenderer, WelcomeRenderer

class UIManager:
    def __init__(self):
        # force_terminal=True ensures Rich generates ANSI codes even if it doesn't detect a real TTY
        self.console = Console(theme=ChatTheme.get_theme(), force_terminal=True)
        self.printer = None

    def set_printer(self, printer_func):
        self.printer = printer_func

    def _print(self, renderable):
        if self.printer:
            with self.console.capture() as capture:
                self.console.print(renderable)
            self.printer(capture.get())
        else:
            self.console.print(renderable)

    def print_message(self, message: Message):
        renderable = MessageRenderer.render(message)
        self._print(renderable)

    def welcome(self):
        self._print(WelcomeRenderer.render())

    def error(self, text: str):
        self._print(f"[error]Error:[/error] {text}")

# Global instance for easy access, or can be instantiated in client
ui = UIManager()
