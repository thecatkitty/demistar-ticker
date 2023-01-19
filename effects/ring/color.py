from ticker.ring import Ring
from .base import RingEffect


class Color(RingEffect):
    _ring: Ring
    _color: tuple[int, int, int]

    def __init__(self, ring: Ring, color: tuple[int, int, int], _) -> None:
        self._ring = ring
        self._color = color

    def start(self) -> None:
        self._ring.fill(*self._color)
