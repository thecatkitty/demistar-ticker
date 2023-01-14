import json
import re

from api import ErrorView, JsonView
from http import HttpRequest, HttpResponse

from ticker.ring import Ring


class RingsProviderInterface:
    def get_ring(self, index: int) -> Ring:
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
        return JsonView([{
            "pixels": ["#{:06X}".format(rgb) for rgb in self._get_pixel_colors(i)]
        } for i in range(2)]).render()

    def post(self, request: HttpRequest) -> HttpResponse:
        print("api.ring: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        if type(data) is not list:
            return ErrorView(422, "Payload is expected to be a list").render()

        for ridx in range(len(data)):
            if type(data[ridx].get("pixels")) is not list:
                return ErrorView(422, "'pixels' is expected to be a list").render()

            pixels = data[ridx].get("pixels")
            ring = self._prings.get_ring(ridx)
            if len(pixels) > len(ring):
                return ErrorView(422, "'pixels' is too long").render()

            for i, rgb in enumerate(pixels):
                if type(rgb) is str and re.match("^#[0-9a-fA-F]+$", rgb):
                    print("api.ring: {}.{} -> {}".format(ridx, i, rgb))
                    ring[i] = tuple(int(rgb[i:(i + 2)], 16) for i in (1, 3, 5))
                    self._prings.rings_changed()

        return JsonView({}).render()

    def _get_pixel_colors(self, index: int) -> list[int]:
        ring = self._prings.get_ring(index)
        return [
            (ring[i][0] << 16) | (ring[i][1] << 8) | ring[i][2]
            for i in range(len(ring))
        ]
