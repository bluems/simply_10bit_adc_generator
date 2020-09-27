import threading
import serial
from math import sin, pi
import struct


class ADCGen:
    def __init__(self, port='COM4', baud=115200, time_sec=0.01):
        self.time_sec = time_sec
        self._gen_range()
        self._calc_sin()
        self.ser = serial.Serial(port, baud, timeout=1)
        self.index = 0

    def _gen_range(self):
        self.x_range = [(self.time_sec * 100) * i / 100 for i in range(-50, 151)]

    def _calc_sin(self):
        self.y_sin = [round((sin(j * pi) + 1) * 0.5 * 1024) for j in self.x_range]

    def _get_y(self):
        self.index = self.index+1 if self.index < len(self.x_range)-1 else 0
        return self.y_sin[self.index]

    def send(self):
        self.ser.write(struct.pack(">H", self._get_y()))
        self.ser.write(b'\x13\x10')
        threading.Timer(self.time_sec, self.send).start()


if __name__ == '__main__':
    gen = ADCGen()
    gen.send()
