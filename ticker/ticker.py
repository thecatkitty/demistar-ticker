import network
import time

from api import ApiProvider
from config import *
from controller.ring import RingsProviderInterface
from http import WebServer, StaticPageProvider
from stage import Board, ManualStage, WallclockStage

from driver.neopixel import Neopixel

from .cefo import CelonesFont
from .ring import Ring
from .manager import StageManager
from .matrix import MatrixDisplay


class DemistarTicker(RingsProviderInterface):
    _server: WebServer
    _manager: StageManager
    _rings_changed: bool
    _board: Board

    def __init__(self, top_display: MatrixDisplay, bottom_display: MatrixDisplay, inner_ring: Ring, outer_ring: Ring) -> None:
        self._board = Board(top_display, bottom_display,
                            inner_ring, outer_ring)

        font = CelonesFont("/ticker/Gidotto8.cefo")
        self._board.top.font = font
        self._board.bottom.font = font

        self._manager = StageManager()
        self._rings_changed = False

    def run(self, port: int) -> None:
        self._server = WebServer(port)
        self._server.add_provider(
            "^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/", ApiProvider({
            "rings_provider": self
        }))

        wallclock = WallclockStage(self._board)

        manual = ManualStage(self._board)
        manual.top = "Lorem ipsum dolor sit amet, consectetur " \
            "adipiscing elit, sed do eiusmod tempor incididunt ut labore " \
            "et dolore magna aliqua."
        manual.bottom = "The quick brown fox jumps over the lazy dog."
        manual.outer = "breath", 64, 0, 32, 2000

        self._manager.stages.append((15, manual))
        self._manager.stages.append((45, wallclock))

        while True:
            self._loop()

    def _loop(self) -> None:
        if self._rings_changed:
            time.sleep_ms(150)
            self._board.bottom.update()
            self._rings_changed = False

        if hasattr(self, "_server"):
            self._server.handle()

        self._manager.handle()

    # Implementation of RingsProviderInterface
    def get_ring(self, index: int) -> Ring:
        return self._board.inner if index == 0 else self._board.outer

    def rings_changed(self) -> None:
        self._rings_changed = True
