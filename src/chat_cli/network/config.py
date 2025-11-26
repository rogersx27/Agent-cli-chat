from pydantic import BaseModel

class NetworkConfig(BaseModel):
    HOST: str = "127.0.0.1"
    PORT: int = 8888
    BUFFER_SIZE: int = 1024
    TIMEOUT: int = 60  # Added a timeout setting as an example of extra config

network_config = NetworkConfig()
