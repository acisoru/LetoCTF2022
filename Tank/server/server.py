import logging
import socket

from camera import Camera
from shared.protocol import Protocol

logging.basicConfig(level=logging.NOTSET, format='%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


class Server:
    def __init__(self):
        self.connection = Protocol.Connection()
        self.camera = Camera()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, self.connection.buffer)

    def __start(self):
        logging.info(f'Starting UDP server {self.connection}')
        self.socket.bind(self.connection.addr())

    def run(self):
        self.__start()
        while True:
            message, client = self.socket.recvfrom(self.connection.buffer)
            logging.info(f'Received {message} from {client}')
            frame = self.camera.read_frame()
            self.socket.sendto(frame, client)


if __name__ == '__main__':
    server = Server()
    server.run()
