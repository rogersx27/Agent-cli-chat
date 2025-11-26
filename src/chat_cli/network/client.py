import asyncio
import sys
from prompt_toolkit import PromptSession, print_formatted_text
from prompt_toolkit.formatted_text import ANSI
from prompt_toolkit.patch_stdout import patch_stdout
from chat_cli.network.config import network_config
from chat_cli.core.types import Message, MessageType, UserMessage, SystemMessage
from chat_cli.core.constants import Commands, UIConstants
from chat_cli.network.protocol import Protocol
from chat_cli.ui.display import ui

class ChatClient:
    def __init__(self, username: str):
        self.username = username
        self.writer: asyncio.StreamWriter | None = None

    async def receive_messages(self, reader: asyncio.StreamReader):
        buffer = b""
        try:
            while True:
                data = await reader.read(network_config.BUFFER_SIZE)
                if not data:
                    ui.error("Server disconnected")
                    break
                
                buffer += data
                while True:
                    result = Protocol.decode_message(buffer)
                    if result is None:
                        break
                    
                    message, remaining = result
                    buffer = remaining
                    ui.print_message(message)
        except asyncio.CancelledError:
            pass

    async def send_messages(self, writer: asyncio.StreamWriter):
        self.writer = writer
        session = PromptSession()
        
        try:
            while True:
                content = await session.prompt_async(UIConstants.PROMPT)
                
                if content.lower() == Commands.QUIT:
                    break
                
                msg = UserMessage(
                    content=content,
                    sender=self.username
                )
                
                encoded = Protocol.encode_message(msg)
                writer.write(encoded)
                await writer.drain()
        except asyncio.CancelledError:
            pass
        except EOFError:
            return
        except KeyboardInterrupt:
            return

    async def start(self):
        try:
            reader, writer = await asyncio.open_connection(network_config.HOST, network_config.PORT)
            
            # Wrap the entire session in patch_stdout so that background prints
            # (from receive_messages) don't mess up the prompt.
            with patch_stdout():
                # Configure UI to use prompt_toolkit's ANSI printer
                ui.set_printer(lambda text: print_formatted_text(ANSI(text)))
                
                ui.welcome()
                ui.print_message(SystemMessage(content=f"Connected to {network_config.HOST}:{network_config.PORT}"))

                receive_task = asyncio.create_task(self.receive_messages(reader))
                send_task = asyncio.create_task(self.send_messages(writer))

                done, pending = await asyncio.wait(
                    [receive_task, send_task],
                    return_when=asyncio.FIRST_COMPLETED
                )

                for task in pending:
                    task.cancel()

            writer.close()
            await writer.wait_closed()
            
        except ConnectionRefusedError:
            ui.error("Could not connect to server")

def run_client(username: str):
    client = ChatClient(username)
    try:
        asyncio.run(client.start())
    except KeyboardInterrupt:
        pass
