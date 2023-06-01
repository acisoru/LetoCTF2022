from base64 import b64encode
from dataclasses import dataclass

import cv2
from imutils import resize


class Camera:
    @dataclass
    class Config:
        width: int = 600
        format: str = '.jpg'
        quality: int = 80

    def __init__(self, source: int = 0):
        self.config = self.Config()
        self.capture = cv2.VideoCapture(source)

    def read_frame(self):
        _, frame = self.capture.read()
        frame = resize(frame, width=self.config.width)
        _, buffer = cv2.imencode(self.config.format, frame, (cv2.IMWRITE_JPEG_QUALITY, self.config.quality))
        return b64encode(buffer)
