import asyncio
import logging
from typing import Set
from chat_cli.network.config import network_config
from chat_cli.core.types import Message, MessageType
from chat_cli.network.protocol import Protocol

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ChatServer:
    def __init__(self):
        self.clients: Set[asyncio.StreamWriter] = set()

    async def handle_client(self, reader: asyncio.StreamReader, writer: asyncio.StreamWriter):
        addr = writer.get_extra_info('peername')
        logger.info(f"New connection from {addr}")
        self.clients.add(writer)

        buffer = b""
        try:
            while True:
                data = await reader.read(network_config.BUFFER_SIZE)
                if not data:
                    break
                
                buffer += data
                
                while True:
                    result = Protocol.decode_message(buffer)
                    if result is None:
                        break
                    
                    message, remaining = result
                    buffer = remaining
                    
                    logger.info(f"Received: {message.content} from {message.sender}")
                    await self.broadcast(message, writer)
                    
        except ConnectionResetError:
            pass
        finally:
            logger.info(f"Connection closed from {addr}")
            self.clients.remove(writer)
            writer.close()
            await writer.wait_closed()

    async def broadcast(self, message: Message, sender_writer: asyncio.StreamWriter):
        encoded = Protocol.encode_message(message)
        for client in self.clients:
            if client != sender_writer:
                try:
                    client.write(encoded)
                    await client.drain()
                except Exception:
                    pass

    async def start(self):
        server = await asyncio.start_server(
            self.handle_client, network_config.HOST, network_config.PORT
        )
        addr = server.sockets[0].getsockname()
        logger.info(f"Serving on {addr}")

        async with server:
            await server.serve_forever()

def run_server():
    server = ChatServer()
    try:
        asyncio.run(server.start())
    except KeyboardInterrupt:
        logger.info("Server stopped")
