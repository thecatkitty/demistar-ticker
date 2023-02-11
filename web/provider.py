from .request import WebRequest
from .response import WebResponse


class ContentProvider:
    def handle_request(self, request: WebRequest) -> WebResponse:
        return WebResponse(404)


class StaticPageProvider(ContentProvider):
    _type: str
    _data: bytes

    def __init__(self, type: str, data: bytes) -> None:
        self._type = type
        self._data = data

    def handle_request(self, request: WebRequest) -> WebResponse:
        if request.method != "GET":
            return WebResponse(405)

        response = WebResponse(200)
        response.headers["Content-Type"] = self._type
        response.data = self._data
        return response
