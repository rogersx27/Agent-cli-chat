from pydantic import BaseModel

class ServerConfig(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 8888
    BUFFER_SIZE: int = 1024

config = ServerConfig()
