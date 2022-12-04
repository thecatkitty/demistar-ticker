import network
import time

from api import ApiProvider
from controller.ring import RingsProviderInterface
from http import WebServer, StaticPageProvider

from driver.neopixel import Neopixel

from .cefo import CelonesFont
from .ring import Ring
from .matrix import MatrixDisplay


class DemistarTicker(RingsProviderInterface):
    _net: network.WLAN
    _server: WebServer
    _font: CelonesFont

    _matrixa: MatrixDisplay
    _matrixb: MatrixDisplay
    _strip: Neopixel
    _rings_changed: bool

    _ringa: Ring
    _ringb: Ring

    def __init__(self) -> None:
        self._font = CelonesFont("/ticker/Gidotto8.cefo")

    def init_network(self, ssid: str, psk: str, retries: int) -> bool:
        self._net = network.WLAN(network.STA_IF)
        self._net.active(True)
        self._net.connect(ssid, psk)

        for i in range(retries):
            if self._net.status() < 0 or self._net.status() >= 3:
                break

            print("trying to connect ({}/{})".format(i + 1, retries))
            self._ringb[i] = 0, 0, 64
            time.sleep(1)

        return self._net.status() == 3

    def init_matrix(self, index: int, spi: int, sck: int, mosi: int, cs: int) -> None:
        if index not in [0, 1]:
            return

        matrix = MatrixDisplay(spi, sck, mosi, cs)
        matrix.font = self._font
        if index == 0:
            self._matrixa = matrix
        else:
            self._matrixb = matrix

    def init_rings(self, length: int, pin: int) -> None:
        self._strip = Neopixel(length, 0, pin, "GRB", delay=0.005)
        self._ringa = Ring(self._strip, 0, 16)
        self._ringb = Ring(self._strip, 16, 16)
        self._strip.clear()
        self._strip.show()

    def init_server(self, port: int) -> str:
        self._server = WebServer(port)
        self._server.add_provider(
            "^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/ring", ApiProvider({
            "rings_provider": self
        }))
        return "{host}:{port}".format(host=self._net.ifconfig()[0], port=port)

    def run(self) -> None:
        while True:
            self._loop()

    def _loop(self) -> None:
        if self._rings_changed:
            time.sleep_ms(150)
            self._strip.show()
            self._rings_changed = False

        if hasattr(self, "_server"):
            self._server.handle()

    def get_matrix(self, index: int) -> MatrixDisplay:
        if index == 0:
            return self._matrixa
        elif index == 1:
            return self._matrixb
        raise IndexError()

    # Implementation of RingsProviderInterface
    def get_ring(self, index: int) -> Ring:
        return self._ringa if index == 0 else self._ringb

    def rings_changed(self) -> None:
        self._rings_changed = True
