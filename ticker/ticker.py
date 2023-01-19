import network
import time

from api import ApiProvider
from config import *
from http import WebServer, StaticPageProvider
from stage import Board, WallclockStage

from .cefo import CelonesFont
from .ring import Ring
from .manager import StageManager
from .matrix import MatrixDisplay


class DemistarTicker:
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
            "board": self._board,
            "stage_manager": self._manager
        }))

        wallclock = WallclockStage(self._board)
        self._manager.add_stage(45, wallclock)

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
