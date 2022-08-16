import json
import re

from http import ContentProvider, HttpRequest, HttpResponse
from neopixel import Neopixel


class DemistarInterface:
    def get_rings(self) -> Neopixel:
        raise NotImplemented()

    def rings_changed(self) -> None:
        raise NotImplemented()


class ApiProvider(ContentProvider):
    _app: DemistarInterface

    def __init__(self, app: DemistarInterface) -> None:
        super().__init__()
        self._app = app

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        if request.method not in ["GET", "POST"]:
            return HttpResponse(405)

        if request.uri.startswith("/ring"):
            return self.handle_ring(request)

        return HttpResponse(404)
 
    def handle_ring(self, request: HttpRequest) -> HttpResponse:
        response = HttpResponse(200)
        response.headers["Content-Type"] = "application/json"

        if request.method == "GET":
            print("api: get ring pixel colors")
            response.data = json.dumps({
                "pixels": ["#{:06X}".format(rgb) for rgb in self.get_pixel_colors()]
            }).encode()
            return response

        print("api: set ring pixel colors")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            response.code = 422
            response.data = json.dumps({
                "error": str(ve)
            }).encode()
            return response

        if type(data.get("pixels")) is not list:
            response.code = 422
            response.data = json.dumps({
                "error": "'pixels' is expected to be a list"
            }).encode()
            return response

        pixels = data.get("pixels")
        rings = self._app.get_rings()
        if len(pixels) > rings.num_leds:
            response.code = 422
            response.data = json.dumps({
                "error": "'pixels' is too long"
            }).encode()
            return response

        for i, rgb in enumerate(pixels):
            if type(rgb) is str and re.match("^#[0-9a-fA-F]+$", rgb):
                print("api: set pixel {} color to {}".format(i, rgb))
                rings.set_pixel(i, [int(rgb[i:(i + 2)], 16) for i in (1, 3, 5)])
                self._app.rings_changed()
        response.data = json.dumps({}).encode()
        return response

    def get_pixel_colors(self):
        rings = self._app.get_rings()
        rsh, gsh, bsh, _ = rings.shift
        return [
            (((pixel >> rsh) & 0xFF) << 16)
                | (((pixel >> gsh) & 0xFF) << 8)
                | ((pixel >> bsh) & 0xFF)
            for pixel in rings.pixels
        ]
