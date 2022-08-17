import network
import socket
import time

from http import WebServer, StaticPageProvider
from neopixel import Neopixel
from api import ApiProvider, DemistarInterface

WHEEL = [
    (0xFF, 0x00, 0x00), (0xFF, 0x55, 0x00), (0xFF, 0xAA, 0x00),
    (0xFF, 0xFF, 0x00), (0xAA, 0xFF, 0x00), (0x55, 0xFF, 0x00),
    (0x00, 0xFF, 0x00), (0x00, 0xFF, 0x55), (0x00, 0xAA, 0xAA),
    (0x00, 0x55, 0xFF), (0x00, 0x00, 0xFF), (0x00, 0x00, 0xFF),
    (0x00, 0x00, 0xFF), (0x55, 0x00, 0xFF), (0xAA, 0x00, 0xFF),
    (0xFF, 0x00, 0xFF)
]

class Demistar(DemistarInterface):
    _net: network.WLAN
    _rings: Neopixel
    _rings_changed: bool
    _server: WebServer

    def init_network(self, ssid: str, psk: str, retries: int) -> bool:
        self._net = network.WLAN(network.STA_IF)
        self._net.active(True)
        self._net.connect(ssid, psk)

        for i in range(retries):
            if self._net.status() < 0 or self._net.status() >= 3:
                break

            print("trying to connect ({i}/{max})".format(
                i = i + 1,
                max = retries))
            time.sleep_ms(500)

        return self._net.status() == 3

    def init_rings(self, length: int, pin: int) -> None:
        self._rings = Neopixel(length, 0, pin, "GRB", delay=0.005)
        self._rings.clear()
        self._rings.show()

        index = 0
        for pixel in WHEEL:
            self._rings.set_pixel(index, (pixel[0] >> 1, pixel[1] >> 1, pixel[2] >> 1))
            index = index + 1

        for pixel in WHEEL:
            self._rings.set_pixel(index, (pixel[0] >> 2, pixel[1] >> 2, pixel[2] >> 2))
            index = index + 1

        self._rings_changed = True

    def init_server(self, port: int) -> str:
        self._server = WebServer(port)
        self._server.add_provider("^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/ring", ApiProvider(self))
        return "{host}:{port}".format(host = self._net.ifconfig()[0], port = port)

    def run(self) -> None:
        while True:
            self._loop()

    def _loop(self) -> None:
        if self._rings_changed:
            time.sleep_ms(50)
            self._rings.show()
            self._rings_changed = False
            time.sleep_ms(50)

        if self._server is not None:
            self._server.handle()

    def set_pixel(self, pixel: int, r: int, g: int, b: int) -> None:
        self._rings.set_pixel(pixel, (r, g, b))

    def get_rings(self) -> Neopixel:
        return self._rings

    def rings_changed(self) -> None:
        self._rings_changed = True
