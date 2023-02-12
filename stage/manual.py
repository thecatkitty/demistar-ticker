from effects import display as dfx
from effects import ring as rfx
from .base import Board, Stage


class ManualStage(Stage):
    top: str
    bottom: str
    inner: tuple
    outer: tuple

    _top: dfx.Marquee
    _bottom: dfx.Marquee
    _inner: rfx.RingEffect
    _outer: rfx.RingEffect

    def __init__(self) -> None:
        self.top = ""
        self.bottom = ""
        self.inner = "color", 0, 0, 0
        self.outer = "color", 0, 0, 0

    def show(self, board: Board) -> None:
        self._top = dfx.Marquee(board.top, board.top.font.print(self.top))
        self._bottom = dfx.Marquee(
            board.bottom, board.bottom.font.print(self.bottom))
        self._inner = rfx.create(
            ring=board.inner,
            name=self.inner[0],
            args=self.inner[1:-1] if self.inner[0] != "color"
            else self.inner[1:],
            time_ms=self.inner[-1])
        self._outer = rfx.create(
            ring=board.outer,
            name=self.outer[0],
            args=self.outer[1:-1] if self.outer[0] != "color"
            else self.outer[1:],
            time_ms=self.outer[-1])

        self._top.start()
        self._bottom.start()
        self._inner.start()
        self._outer.start()

    def update(self, board: Board) -> None:
        self._top.update()
        self._bottom.update()
        self._inner.update()
        self._outer.update()

    def to_dict(self) -> dict:
        return {
            "name": "manual",
            "top": self.top,
            "bottom": self.bottom,
            "inner": self.inner,
            "outer": self.outer
        }

    @staticmethod
    def from_dict(o: dict) -> object:
        stage = ManualStage()

        top = o.get("top")
        if type(top) is str:
            stage.top = top

        bottom = o.get("bottom")
        if type(bottom) is str:
            stage.bottom = bottom

        inner = o.get("inner")
        if type(inner) is list:
            stage.inner = tuple(inner)

        outer = o.get("outer")
        if type(outer) is list:
            stage.outer = tuple(outer)

        return stage
