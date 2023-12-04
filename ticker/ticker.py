import machine
import network
import time

from api import ApiProvider
from config import *
from stage import Board, WallclockStage
from web import WebServer, StaticPageProvider

from .cefo import CelonesFont
from .manager import StageManager
from .timeline import Timeline


class DemistarTicker:
    _network: network.WLAN
    _server: WebServer
    _manager: StageManager

    _last_net_check: int

    NET_STAT_DESCRIPTIONS = {
        network.STAT_IDLE: "network idle",
        network.STAT_CONNECTING: "connecting",
        network.STAT_CONNECT_FAIL: "connect fail",
        network.STAT_NO_AP_FOUND: "no AP found",
        network.STAT_WRONG_PASSWORD: "wrong password"
    }

    def __init__(self, board: Board) -> None:
        font = CelonesFont("/ticker/Gidotto8.cefo")
        board.top.font = font
        board.bottom.font = font

        self._manager = StageManager(board)

    def run(self, port: int) -> None:
        self._network = network.WLAN(network.STA_IF)
        self._last_net_check = time.ticks_ms()

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
        now = time.ticks_ms()
        if time.ticks_diff(now, self._last_net_check) > 1000:
            self._last_net_check = now
            if not self._network.isconnected():
                status = self._network.status()
                print("net:", DemistarTicker.NET_STAT_DESCRIPTIONS[status])
                if status != network.STAT_CONNECTING:
                    print("net: connecting...")
                    self._network.connect(LOCAL["wlan"]["ssid"], LOCAL["wlan"]["psk"])

        if hasattr(self, "_server"):
            self._server.handle()

        self._manager.handle()
