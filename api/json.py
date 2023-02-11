import json

from web import WebResponse


class JsonResponse(WebResponse):
    def __init__(self, model: dict, status: int = 200) -> None:
        super().__init__(status)
        self.headers["Content-Type"] = "application/json"
        self.data = json.dumps(model).encode()
