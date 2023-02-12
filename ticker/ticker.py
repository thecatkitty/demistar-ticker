from api import ApiProvider
from config import *
from stage import Board, WallclockStage
from web import WebServer, StaticPageProvider

from .cefo import CelonesFont
from .manager import StageManager
from .timeline import Timeline


class DemistarTicker:
    _server: WebServer
    _manager: StageManager

    def __init__(self, board: Board) -> None:
        font = CelonesFont("/ticker/Gidotto8.cefo")
        board.top.font = font
        board.bottom.font = font

        self._manager = StageManager(board)

    def run(self, port: int) -> None:
        self._server = WebServer(port)
        self._server.add_provider(
            "^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/", ApiProvider({
            "stage_manager": self._manager
        }))

        if len(Timeline._storage) == 0:
            wallclock = WallclockStage()
            self._manager.add_stage(45, wallclock)

        while True:
            self._loop()

    def _loop(self) -> None:
        if hasattr(self, "_server"):
            self._server.handle()

        self._manager.handle()
