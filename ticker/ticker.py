import machine
import network
import time

from api import ApiProvider, convert
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
    _port: int

    _last_net_check: int
    _last_time_save: int

    TIME_SAVE = "/data/timesave.txt"

    def __init__(self, board: Board) -> None:
        font = CelonesFont("/ticker/Gidotto8.cefo")
        board.top.font = font
        board.bottom.font = font

        self._manager = StageManager(board)

    def _save_time(self) -> None:
        saved_time = convert.time_to_string(time.time())
        with open(DemistarTicker.TIME_SAVE, "w") as file:
            file.write(saved_time)
            print("ticker: saved time {}".format(saved_time))

    def _load_time(self) -> None:
        saved_time = "2021-01-01T00:00:00"
        try:
            with open(DemistarTicker.TIME_SAVE, "r") as file:
                saved_time = file.readline()

        except OSError:
            print("ticker: no saved time!")

        print("ticker: restored time {}".format(saved_time))
        timestamp = convert.string_to_time(saved_time)
        year, month, mday, hour, minute, second, _, _ = time.localtime(
            timestamp)
        machine.RTC().datetime((year, month, mday, 0, hour, minute, second, 0))

    def _start_server(self) -> None:
        print("net: address {}".format(self._network.ifconfig()[0]))
        self._server = WebServer(self._port)
        self._server.add_provider(
            "^/$", StaticPageProvider("text/html", "<h1>It works!</h1>".encode()))
        self._server.add_provider("^/", ApiProvider({
            "stage_manager": self._manager
        }))

    def run(self, port: int) -> None:
        now = time.ticks_ms()
        self._last_net_check = now
        self._last_time_save = now

        self._network = network.WLAN(network.STA_IF)
        self._port = port

        self._load_time()

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
                print("net: status", status)
                if status != network.STAT_CONNECTING:
                    print("net: connecting...")
                    self._network.connect(
                        LOCAL["wlan"]["ssid"], LOCAL["wlan"]["psk"])

        if time.ticks_diff(now, self._last_time_save) > 180000:
            self._last_time_save = now
            self._save_time()

        if hasattr(self, "_server"):
            self._server.handle()
        elif self._network.isconnected():
            self._start_server()

        self._manager.handle()
