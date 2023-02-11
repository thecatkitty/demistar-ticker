import sys

from web import ContentProvider, WebRequest, WebResponse


class ApiProvider(ContentProvider):
    _deps: dict

    def __init__(self, deps: dict) -> None:
        super().__init__()
        self._deps = deps

    def handle_request(self, request: WebRequest) -> WebResponse:
        import controller
        parts = request.uri.split("/")
        if parts[1] not in dir(controller):
            return WebResponse(404)

        ctrl_name = parts[1][0].upper() + parts[1][1:] + "Controller"
        try:
            ctrl_class = getattr(
                sys.modules["controller.{}".format(parts[1])], ctrl_name)
        except Exception as e:
            print("api: ", str(e))
            return WebResponse(500)

        if request.method.lower() not in dir(ctrl_class):
            return WebResponse(405)

        if ctrl_class.dependencies is None:
            ctrl = ctrl_class()
        else:
            ctrl_deps = [self._deps[dep] for dep in ctrl_class.dependencies]
            ctrl = ctrl_class(*ctrl_deps)

        return getattr(ctrl, request.method.lower())(request)
