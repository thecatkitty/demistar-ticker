import network
import time

from api import ApiProvider
from config import *
from controller.ring import RingsProviderInterface
from http import WebServer, StaticPageProvider
from stage.wallclock import WallclockStage

from driver.neopixel import Neopixel

from .cefo import CelonesFont
from .ring import Ring
from .matrix import MatrixDisplay


class DemistarTicker(RingsProviderInterface):
    _net: network.WLAN
    _server: WebServer

    _top: MatrixDisplay
    _bottom: MatrixDisplay
    _strip: Neopixel
    _rings_changed: bool

    _inner: Ring
    _outer: Ring

    _stage: WallclockStage

    def __init__(self, top_display: MatrixDisplay, bottom_display: MatrixDisplay, inner_ring: Ring, outer_ring: Ring) -> None:
        self._top = top_display
        self._bottom = bottom_display
        self._inner = inner_ring
        self._outer = outer_ring

        font = CelonesFont("/ticker/Gidotto8.cefo")
        self._top.font = font
        self._bottom.font = font

        self._rings_changed = False

    def run(self, port: int) -> None:
        self._server = WebServer(port)
        self._server.add_provider(
            "^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/", ApiProvider({
            "rings_provider": self
        }))

        print("ticker: setting the stage")
        self._stage = WallclockStage(
            self._top, self._bottom, self._inner, self._outer)

        while True:
            self._loop()

    def _loop(self) -> None:
        if self._rings_changed:
            time.sleep_ms(150)
            self._bottom.update()
            self._rings_changed = False

        if hasattr(self, "_server"):
            self._server.handle()

        self._stage.update()

    # Implementation of RingsProviderInterface
    def get_ring(self, index: int) -> Ring:
        return self._inner if index == 0 else self._outer

    def rings_changed(self) -> None:
        self._rings_changed = True
