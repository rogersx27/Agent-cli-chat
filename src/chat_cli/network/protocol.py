import struct
from typing import Optional
from pydantic import TypeAdapter
from chat_cli.core.types import Message
from chat_cli.core.constants import ProtocolConstants

# Adapter to handle polymorphic Message types
message_adapter = TypeAdapter(Message)

class Protocol:
    @staticmethod
    def encode_message(message: Message) -> bytes:
        """Encodes a message to bytes with a length header."""
        # model_dump_json produces the JSON string
        json_str = message_adapter.dump_json(message).decode(ProtocolConstants.ENCODING)
        message_bytes = json_str.encode(ProtocolConstants.ENCODING)
        # Prefix with 4-byte length
        return struct.pack(ProtocolConstants.HEADER_FORMAT, len(message_bytes)) + message_bytes

    @staticmethod
    def decode_message(data: bytes) -> Optional[tuple[Message, bytes]]:
        """
        Decodes a message from the buffer.
        Returns (Message, remaining_bytes) if a full message is found, else None.
        """
        if len(data) < ProtocolConstants.HEADER_SIZE:
            return None
        
        msg_len = struct.unpack(ProtocolConstants.HEADER_FORMAT, data[:ProtocolConstants.HEADER_SIZE])[0]
        if len(data) < ProtocolConstants.HEADER_SIZE + msg_len:
            return None
            
        msg_data = data[ProtocolConstants.HEADER_SIZE:ProtocolConstants.HEADER_SIZE + msg_len]
        remaining = data[ProtocolConstants.HEADER_SIZE + msg_len:]
        
        try:
            # validate_json parses the JSON bytes/string and returns the correct model instance
            message = message_adapter.validate_json(msg_data)
            return message, remaining
        except Exception:
            return None
