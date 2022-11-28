import json
import re

from http import HttpRequest, HttpResponse
from view import ErrorView, JsonView

from driver.neopixel import Neopixel


class RingsProviderInterface:
    def get_rings(self) -> Neopixel:
        raise NotImplementedError()

    def rings_changed(self) -> None:
        raise NotImplementedError()


class RingController:
    dependencies = ["rings_provider"]

    _prings: RingsProviderInterface

    def __init__(self, rings_provider: RingsProviderInterface) -> None:
        self._prings = rings_provider

    def get(self, request: HttpRequest) -> HttpResponse:
        print("api.ring: get")
        return JsonView({
            "pixels": ["#{:06X}".format(rgb) for rgb in self._get_pixel_colors()]
        }).render()

    def post(self, request: HttpRequest) -> HttpResponse:
        print("api.ring: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        if type(data.get("pixels")) is not list:
            return ErrorView(422, "'pixels' is expected to be a list").render()

        pixels = data.get("pixels")
        rings = self._prings.get_rings()
        if len(pixels) > rings.num_leds:
            return ErrorView(422, "'pixels' is too long").render()

        for i, rgb in enumerate(pixels):
            if type(rgb) is str and re.match("^#[0-9a-fA-F]+$", rgb):
                print("api: set pixel {} color to {}".format(i, rgb))
                rings.set_pixel(i,[int(rgb[i:(i + 2)], 16) for i in (1, 3, 5)])
                self._prings.rings_changed()
        return JsonView({}).render()

    def _get_pixel_colors(self):
        rings = self._prings.get_rings()
        rsh, gsh, bsh, _ = rings.shift
        return [
            (((pixel >> rsh) & 0xFF) << 16)
                | (((pixel >> gsh) & 0xFF) << 8)
                | ((pixel >> bsh) & 0xFF)
            for pixel in rings.pixels
        ]
