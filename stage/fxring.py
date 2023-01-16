import utime

from ticker.ring import Ring


class Blink:
    _ring: Ring
    _color: tuple[int, int, int]

    _interval: int
    _time: int
    _bright: bool

    def __init__(self, ring: Ring, color: tuple[int, int, int], interval_ms: int) -> None:
        self._ring = ring
        self._color = color
        self._interval = interval_ms

    def start(self) -> None:
        self._bright = False
        self._time = utime.ticks_add(utime.ticks_ms(), self._interval)

    def update(self) -> None:
        if utime.ticks_diff(utime.ticks_ms(), self._time) < 0:
            return

        self._time = utime.ticks_add(utime.ticks_ms(), self._interval)
        if self._bright:
            self._ring.fill(0, 0, 0)
        else:
            self._ring.fill(*self._color)

        self._bright = not self._bright
