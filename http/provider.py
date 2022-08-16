from .request import HttpRequest
from .response import HttpResponse


class ContentProvider:
    def handle_request(self, request: HttpRequest) -> HttpResponse:
        return HttpResponse(404)


class StaticPageProvider(ContentProvider):
    _type: str
    _data: bytes

    def __init__(self, type: str, data: bytes) -> None:
        self._type = type
        self._data = data

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        if request.method != "GET":
            return HttpResponse(405)

        response = HttpResponse(200)
        response.headers["Content-Type"] = self._type
        response.data = self._data
        return response
