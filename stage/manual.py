from effects import display as dfx
from effects import ring as rfx
from .base import Board, Stage


class ManualStage(Stage):
    top: str
    bottom: str
    inner: tuple[str, int, int, int, int]
    outer: tuple[str, int, int, int, int]

    _b: Board
    _top: dfx.Marquee
    _bottom: dfx.Marquee
    _inner: rfx.RingEffect
    _outer: rfx.RingEffect

    def __init__(self, board: Board) -> None:
        self._b = board
        self.top = ""
        self.bottom = ""
        self.inner = "blink", 64, 64, 64, 500
        self.outer = "blink", 64, 64, 64, 500

    def show(self) -> None:
        self._top = dfx.Marquee(self._b.top, self._b.top.font.print(self.top))
        self._bottom = dfx.Marquee(
            self._b.bottom, self._b.bottom.font.print(self.bottom))
        self._inner = rfx.create(
            ring=self._b.inner,
            name=self.inner[0],
            args=self.inner[1:-1],
            time_ms=self.inner[-1])
        self._outer = rfx.create(
            ring=self._b.outer,
            name=self.outer[0],
            args=self.outer[1:-1],
            time_ms=self.outer[-1])

        self._top.start()
        self._bottom.start()
        self._inner.start()
        self._outer.start()

    def update(self) -> None:
        self._top.update()
        self._bottom.update()
        self._inner.update()
        self._outer.update()
