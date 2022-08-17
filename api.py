import sys

import controller

from controller.ring import RingsProviderInterface
from http import ContentProvider, HttpRequest, HttpResponse


class ApiProvider(ContentProvider):
    _prings: RingsProviderInterface

    def __init__(self, rings_provider: RingsProviderInterface) -> None:
        super().__init__()
        self._prings = rings_provider

    def handle_request(self, request: HttpRequest) -> HttpResponse:
        parts = request.uri.split("/")
        if parts[1] not in dir(controller):
            return HttpResponse(404)

        ctrl_name = parts[1][0].upper() + parts[1][1:] + "Controller"
        try:
            ctrl_class = getattr(sys.modules["controller.{}".format(parts[1])], ctrl_name)
        except Exception as e:
            print("api: ", str(e))
            return HttpResponse(500)

        if request.method.lower() not in dir(ctrl_class):
            return HttpResponse(405)

        ctrl = ctrl_class(self._prings)
        return getattr(ctrl, request.method.lower())(request)
