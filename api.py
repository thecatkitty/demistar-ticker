import json
import re

from controller.ring import RingsProviderInterface
from http import ContentProvider, HttpRequest, HttpResponse
from view import ErrorView, JsonView


class ApiProvider(ContentProvider):
    _prings: RingsProviderInterface

    def __init__(self, rings_provider: RingsProviderInterface) -> None:
        super().__init__()
        self._prings = rings_provider

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        if request.method not in ["GET", "POST"]:
            return HttpResponse(405)

        if request.uri.startswith("/ring"):
            return self.handle_ring(request)

        return HttpResponse(404)
 
    def handle_ring(self, request: HttpRequest) -> HttpResponse:
        if request.method == "GET":
            print("api: get ring pixel colors")
            return JsonView({
                "pixels": ["#{:06X}".format(rgb) for rgb in self.get_pixel_colors()]
            }).render()

        print("api: set ring pixel colors")
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

    def get_pixel_colors(self):
        rings = self._prings.get_rings()
        rsh, gsh, bsh, _ = rings.shift
        return [
            (((pixel >> rsh) & 0xFF) << 16)
                | (((pixel >> gsh) & 0xFF) << 8)
                | ((pixel >> bsh) & 0xFF)
            for pixel in rings.pixels
        ]
