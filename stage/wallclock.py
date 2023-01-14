import time

from config import *
from ticker.matrix import MatrixDisplay
from ticker.ring import Ring


class WallclockStage:
    _top: MatrixDisplay
    _bottom: MatrixDisplay
    _inner: Ring
    _outer: Ring
    _last_sec: int

    def __init__(self, top_display: MatrixDisplay, bottom_display: MatrixDisplay, inner_ring: Ring, outer_ring: Ring) -> None:
        self._top = top_display
        self._bottom = bottom_display
        self._inner = inner_ring
        self._outer = outer_ring
        self._last_sec = -1

    def show(self):
        self._last_sec = -1

    def update(self):
        timestamp = time.localtime()
        if timestamp[5] == self._last_sec:
            return

        self._top.clear()
        self._top.draw_text(
            "{3:02}:{4:02}:{5:02}".format(*timestamp))
        self._top.update()

        self._bottom.clear()
        self._bottom.draw_text(WEEKDAYS[timestamp[6]])
        self._bottom.update()

        self._outer._strip.fill((0, 0, 0))
        self._outer._strip.set_pixel_line(
            0, round((timestamp[3] % 12) * 16 / 12), (3, 0, 2))
        self._outer._strip.set_pixel_line(
            16, 16 + round(timestamp[4] * 16 / 60), (3, 2, 0))
        self._outer._strip.show()

        self._last_sec = timestamp[5]
