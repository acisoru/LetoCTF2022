from enum import Enum


class Protocol:
    class Connection:
        ip: str = '127.0.0.1'
        port: int = 31337
        buffer: int = 65536

        def addr(self) -> tuple[str, int]:
            return self.ip, self.port

        def __repr__(self) -> str:
            return f'{self.ip}:{self.port}'

    class Command(Enum):
        LEFT = b'LEFT'
        RIGHT = b'RIGHT'
        FORWARD = b'FORWARD'
        BACKWARD = b'BACKWARD'
        ROTATE_LEFT = b'ROTATE LEFT'
        ROTATE_RIGHT = b'ROTATE RIGHT'
