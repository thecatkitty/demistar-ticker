import time

from effects import display as dfx
from effects import ring as rfx

from .base import Board, Stage


class MeetingStage(Stage):
    title: str
    host: str
    start: tuple
    end: tuple

    _top: dfx.Marquee
    _bottom: dfx.Marquee
    _inner: rfx.RingEffect
    _outer: rfx.RingEffect

    def __init__(self) -> None:
        self.title = ""
        self.host = ""
        self.start = time.localtime(time.time())
        self.end = time.localtime(time.time() + 3600)

    def show(self, board: Board) -> None:
        self._top = dfx.Marquee(board.top, board.top.font.print(self.title))
        self._bottom = dfx.Marquee(board.bottom, board.bottom.font.print(
            "{:02}:{:02}-{:02}:{:02}, {}".format(self.start[3], self.start[4], self.end[3], self.end[4], self.host)))
        self._inner = rfx.create(board.inner, "breath", (0, 16, 0), 5000)

        self._top.start()
        self._bottom.start()
        self._inner.start()
        board.outer.fill(0, 0, 0)

    def update(self, board: Board) -> None:
        self._top.update()
        self._bottom.update()
        self._inner.update()

        now_epoch = time.time()
        start_epoch = time.mktime(self.start)
        end_epoch = time.mktime(self.end)
        completion = (now_epoch - start_epoch) / (end_epoch - start_epoch)
        hand = round(completion * 16)
        board.outer.fill(0, 0, 0, False)
        board.outer.put_line(3, 0, 2, 0, hand, True)

    def to_dict(self) -> dict:
        return {
            "name": "manual",
            "title": self.title,
            "host": self.host
        }

    @staticmethod
    def from_dict(o: dict):
        stage = MeetingStage()

        title = o.get("title")
        if type(title) is str:
            stage.title = title

        host = o.get("host")
        if type(host) is str:
            stage.host = host

        return stage
