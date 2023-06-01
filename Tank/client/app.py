from __future__ import annotations

import tkinter.ttk as ttk
from base64 import b64decode
from dataclasses import dataclass
from io import BytesIO
from tkinter import *
from PIL import Image, ImageTk

from client import Client
from shared.protocol import Protocol

COMMANDS = {
    'Q': Protocol.Command.ROTATE_LEFT,
    'W': Protocol.Command.FORWARD,
    'E': Protocol.Command.ROTATE_RIGHT,
    'A': Protocol.Command.LEFT,
    'S': Protocol.Command.BACKWARD,
    'D': Protocol.Command.RIGHT
}


def load_image(image: str, size: tuple[int, int]):
    image = Image.open(f'./images/{image}')
    image.thumbnail(size)
    return ImageTk.PhotoImage(image)


def decode_image(encoded: bytes, size: tuple[int, int]):
    decoded = BytesIO(b64decode(encoded))
    image = Image.open(decoded)
    image.thumbnail(size)
    return ImageTk.PhotoImage(image)


@dataclass
class AppConfig:
    width: int = 900
    height: int = 700
    title: str = 'Tank control'

    @staticmethod
    def geometry():
        return '{}x{}'.format(AppConfig.width, AppConfig.height)


class CameraFrame(ttk.Frame):
    def __init__(self, master: Tk):
        super().__init__(master)
        image = load_image('noise.png', (AppConfig.width, AppConfig.height * 2 // 3))
        self.label = ttk.Label(self, padding=10, image=image)
        self.label.imgtk = image
        self.label.pack()

    def refresh(self, frame: bytes):
        image = decode_image(frame, (AppConfig.width, AppConfig.height * 2 // 3))
        self.label.config(image=image)
        self.label.imgtk = image


class ButtonFrame(ttk.Frame):
    def __init__(self, master: ttk.Frame, main: MainApplication, **kwargs):
        super().__init__(master)
        self.button = ttk.Button(self, padding=8, style='my.TButton', **kwargs)
        self.button.bind('<Button-1>', lambda event: main.on_click(kwargs['text']))
        self.button.pack()


class ControlsFrame(ttk.Frame):
    def __init__(self, master: MainApplication):
        super().__init__(master)
        self.buttons = [
            ButtonFrame(self, master, text='Q'),
            ButtonFrame(self, master, text='W'),
            ButtonFrame(self, master, text='E'),
            ButtonFrame(self, master, text='A'),
            ButtonFrame(self, master, text='S'),
            ButtonFrame(self, master, text='D')
        ]
        for i, button in enumerate(self.buttons):
            button.grid(column=i % 3, row=i // 3, padx=4, pady=4)


class MainApplication(Tk):
    def __init__(self):
        super().__init__()
        ttk.Style().configure('my.TButton', font=(None, 12))
        self.client = Client()
        self.camera = CameraFrame(self)
        self.controls = ControlsFrame(self)
        self.config()
        self.bind_keys()
        self.pack_slaves()

    def bind_keys(self):
        self.bind('q', lambda event: self.on_click('Q'))
        self.bind('w', lambda event: self.on_click('W'))
        self.bind('e', lambda event: self.on_click('E'))
        self.bind('a', lambda event: self.on_click('A'))
        self.bind('s', lambda event: self.on_click('S'))
        self.bind('d', lambda event: self.on_click('D'))

    def config(self):
        self.title(AppConfig.title)
        self.geometry(AppConfig.geometry())
        self.state('zoomed')

    def pack_slaves(self):
        self.camera.pack()
        self.controls.pack()

    def on_click(self, event: str):
        frame = self.client.communicate(COMMANDS[event])
        self.camera.refresh(frame)


if __name__ == '__main__':
    app = MainApplication()
    app.mainloop()
