import network
import socket
import time

from http import WebServer, StaticPageProvider
from neopixel import Neopixel
from api import ApiProvider, DemistarInterface


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

            print("trying to connect ({}/{})".format(i + 1, retries))
            self.set_pixel(16 + i, 0, 0, 64)
            self._rings.show()
            time.sleep(1)

        return self._net.status() == 3

    def init_rings(self, length: int, pin: int) -> None:
        self._rings = Neopixel(length, 0, pin, "GRB", delay=0.005)
        self._rings.clear()
        self._rings.show()

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
