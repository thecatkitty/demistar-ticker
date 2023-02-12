import time

from config import *

import lang
from .base import Board, Stage


class WallclockStage(Stage):
    _last_sec: int

    def __init__(self) -> None:
        self._last_sec = -1

    def show(self, board: Board) -> None:
        self._last_sec = -1

    def update(self, board: Board) -> None:
        timestamp = time.localtime()
        if timestamp[5] == self._last_sec:
            return

        if timestamp[0] < 2023:
            board.top.clear()
            board.top.draw_text("wrong date")
            board.top.update()

            board.bottom.clear()
            board.bottom.draw_text("POST wallclock")
            board.bottom.update()

            if timestamp[5] % 2 == 0:
                board.inner.fill(3, 1, 0, False)
                board.outer.fill(0, 0, 0, False)
            else:
                board.inner.fill(0, 0, 0, False)
                board.outer.fill(3, 1, 0, False)
            board.inner.update()
            return

        board.top.clear()
        board.top.draw_text(
            "{3:02}:{4:02}:{5:02}".format(*timestamp))
        board.top.update()

        bottom_text = lang.WEEKDAYS[timestamp[6]]
        if self._last_sec >= 45:
            bottom_text = lang.FMT_DATE.format(
                month_name=lang.MONTHS[timestamp[1] - 1],
                day=timestamp[2])

        board.bottom.clear()
        board.bottom.draw_text(bottom_text, x=-1)
        board.bottom.update()

        minute_hand = round(timestamp[4] * 16 / 60)
        board.inner.fill(0, 0, 0, False)
        board.inner.put_line(3, 0, 2, 0, minute_hand, False)

        hour_hand = round((timestamp[3] % 12) * 16 / 12)
        board.outer.fill(0, 0, 0, False)
        board.outer.put_line(3, 2, 0, 0, hour_hand, False)

        board.inner.update()
        self._last_sec = timestamp[5]

    def to_dict(self) -> dict:
        return {
            "name": "wallclock"
        }
    
    @staticmethod
    def from_dict(o: dict) -> object:
        return WallclockStage()
