import socket

from shared.protocol import Protocol


class Client:
    def __init__(self):
        self.connection = Protocol.Connection()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.connection.buffer)

    def communicate(self, command: Protocol.Command) -> bytes:
        self.socket.sendto(command.value, self.connection.addr())
        packet, _ = self.socket.recvfrom(self.connection.buffer)
        return packet
