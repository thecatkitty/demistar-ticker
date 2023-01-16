from framebuf import FrameBuffer, MONO_VLSB
from machine import Pin, SPI

from driver.max7219.max7219 import Matrix8x8

from .cefo import CelonesFont


class MatrixDisplay:
    font: CelonesFont

    _ctl: Matrix8x8

    def __init__(self, spi: int, sck: int, mosi: int, cs: int) -> None:
        self._ctl = Matrix8x8(
            SPI(spi, sck=Pin(sck), mosi=Pin(mosi)), Pin(cs), 8)

    def clear(self) -> None:
        self._ctl.fill(0)

    def draw(self, fbuf: FrameBuffer, x: int = 0) -> None:
        self._ctl.blit(fbuf, x, 0)

    def draw_text(self, text: str, font=None, x: int = 0) -> None:
        if font is None:
            font = self.font

        pixels = font.print(text)
        if pixels is None:
            return

        if x < 0:
            x = 65 + x - len(pixels)

        self.draw(FrameBuffer(pixels, len(pixels), 8, MONO_VLSB), x)

    def update(self) -> None:
        self._ctl.show()
