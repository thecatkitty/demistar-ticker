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

        bottom_text = WEEKDAYS[timestamp[6]]
        if self._last_sec >= 45:
            bottom_text = FMT_DATE.format(
                month_name=MONTHS[timestamp[1] - 1],
                day=timestamp[2])

        self._bottom.clear()
        self._bottom.draw_text(bottom_text, x=-1)
        self._bottom.update()

        minute_hand = round((timestamp[3] % 12) * 16 / 12)
        self._inner.fill(0, 0, 0, False)
        self._inner.put_line(3, 0, 2, 0, minute_hand, False)

        hour_hand = round(timestamp[4] * 16 / 60)
        self._outer.fill(0, 0, 0, False)
        self._outer.put_line(3, 2, 0, 0, hour_hand, False)

        self._inner.update()
        self._last_sec = timestamp[5]
