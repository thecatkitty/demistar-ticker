import utime
from framebuf import FrameBuffer, MONO_VLSB

from ticker.matrix import MatrixDisplay


class Marquee:
    _display: MatrixDisplay
    _bitmap: FrameBuffer
    _width: int

    _offset: int
    _interval: int
    _time: int

    def __init__(self, display: MatrixDisplay, pixels: bytearray) -> None:
        if pixels is None:
            pixels = bytearray()

        self._display = display
        self._bitmap = FrameBuffer(pixels, len(pixels), 8, MONO_VLSB)
        self._width = len(pixels)

        self._offset = 0
        self._interval = None  # type: ignore

    def start(self) -> None:
        if self._width > 64:
            self._offset = 64
            self._interval = 80  # 5.12 seconds per screen
            self._time = utime.ticks_add(utime.ticks_ms(), self._interval)

        self._display.clear()
        self._display.draw(self._bitmap, self._offset)
        self._display.update()

    def update(self) -> None:
        if self._interval is None:
            return

        if utime.ticks_diff(utime.ticks_ms(), self._time) < 0:
            return

        self._time = utime.ticks_add(utime.ticks_ms(), self._interval)
        self._display.clear()
        self._display.draw(self._bitmap, self._offset)
        self._display.update()
        self._offset -= 1

        if self._offset == -self._width:
            self._offset = 64
