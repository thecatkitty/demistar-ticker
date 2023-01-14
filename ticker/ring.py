from driver.neopixel import Neopixel


class Ring:
    _strip: Neopixel
    _start: int
    _length: int

    def __init__(self, strip: Neopixel, start: int, length: int) -> None:
        if start > strip.num_leds:
            raise ValueError()

        if start + length > strip.num_leds:
            raise ValueError()

        self._strip = strip
        self._start = start
        self._length = length

    def __len__(self) -> int:
        return self._length

    def __getitem__(self, index: int) -> tuple[int, int, int]:
        rsh, gsh, bsh, _ = self._strip.shift
        pixel = self._strip.pixels[self._start + index]
        return ((pixel >> rsh) & 0xFF), ((pixel >> gsh) & 0xFF), (pixel >> bsh) & 0xFF

    def __setitem__(self, index: int, value: tuple[int, int, int]) -> None:
        rsh, gsh, bsh, _ = self._strip.shift
        pixel = (value[0] << rsh) | (value[1] << gsh) | (value[2] << bsh)
        self._strip.pixels[self._start + index] = pixel
        self.update()

    def fill(self, r: int, g: int, b: int, update: bool = True):
        self.put_line(r, g, b, 0, self._length, update)

    def put_line(self, r: int, g: int, b: int, start: int, length: int, update: bool = True):
        rsh, gsh, bsh, _ = self._strip.shift
        pixel = (r << rsh) | (g << gsh) | (b << bsh)
        for i in range(self._start + start, self._start + start + length):
            self._strip.pixels[i] = pixel

        if update:
            self.update()

    def update(self):
        self._strip.show()
