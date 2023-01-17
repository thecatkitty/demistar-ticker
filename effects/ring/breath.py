import utime

from ticker.ring import Ring
from .base import RingEffect


class Breath(RingEffect):
    _ring: Ring
    _color: tuple[int, int, int]
    _cycle: int

    _db: float
    _dt: int
    _brightness: float
    _time: int

    def __init__(self, ring: Ring, color: tuple[int, int, int], cycle_ms: int) -> None:
        self._ring = ring
        self._color = color
        self._cycle = cycle_ms

    def start(self) -> None:
        steps = max(self._color)
        self._db = 1 / steps
        self._dt = round(self._cycle / 2 / steps)
        self._brightness = 0.0
        self._time = utime.ticks_add(utime.ticks_ms(), self._dt)

    def update(self) -> None:
        if utime.ticks_diff(utime.ticks_ms(), self._time) < 0:
            return

        self._time = utime.ticks_add(utime.ticks_ms(), self._dt)
        self._ring.fill(
            round(self._brightness * self._color[0]),
            round(self._brightness * self._color[1]),
            round(self._brightness * self._color[2]))

        self._brightness += self._db
        if self._brightness <= 0 or self._brightness >= 1:
            self._db = -self._db
