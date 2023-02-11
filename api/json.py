from web import WebResponse
from . import convert


class JsonResponse(WebResponse):
    def __init__(self, model: dict, status: int = 200) -> None:
        super().__init__(status)
        self.headers["Content-Type"] = "application/json"
        self.data = model  # type: ignore

    def get_bytes(self):
        return convert.to_json_bytes(self.data)
