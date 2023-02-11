import time

from config import *

import lang
from .base import Board, Stage


class WallclockStage(Stage):
    _b: Board
    _last_sec: int

    def __init__(self, board: Board) -> None:
        self._b = board
        self._last_sec = -1

    def show(self) -> None:
        self._last_sec = -1

    def update(self) -> None:
        timestamp = time.localtime()
        if timestamp[5] == self._last_sec:
            return

        if timestamp[0] < 2023:
            self._b.top.clear()
            self._b.top.draw_text("wrong date")
            self._b.top.update()

            self._b.bottom.clear()
            self._b.bottom.draw_text("POST wallclock")
            self._b.bottom.update()

            if timestamp[5] % 2 == 0:
                self._b.inner.fill(3, 1, 0, False)
                self._b.outer.fill(0, 0, 0, False)
            else:
                self._b.inner.fill(0, 0, 0, False)
                self._b.outer.fill(3, 1, 0, False)
            self._b.inner.update()
            return

        self._b.top.clear()
        self._b.top.draw_text(
            "{3:02}:{4:02}:{5:02}".format(*timestamp))
        self._b.top.update()

        bottom_text = lang.WEEKDAYS[timestamp[6]]
        if self._last_sec >= 45:
            bottom_text = lang.FMT_DATE.format(
                month_name=lang.MONTHS[timestamp[1] - 1],
                day=timestamp[2])

        self._b.bottom.clear()
        self._b.bottom.draw_text(bottom_text, x=-1)
        self._b.bottom.update()

        minute_hand = round(timestamp[4] * 16 / 60)
        self._b.inner.fill(0, 0, 0, False)
        self._b.inner.put_line(3, 0, 2, 0, minute_hand, False)

        hour_hand = round((timestamp[3] % 12) * 16 / 12)
        self._b.outer.fill(0, 0, 0, False)
        self._b.outer.put_line(3, 2, 0, 0, hour_hand, False)

        self._b.inner.update()
        self._last_sec = timestamp[5]

    def to_dict(self) -> dict:
        return {
            "name": "wallclock"
        }
    
    @staticmethod
    def from_dict(board: Board, o: dict) -> object:
        return WallclockStage(board)
