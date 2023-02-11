import json

from web import WebResponse
from .basic import BasicView


class JsonView(BasicView):
    def __init__(self, model, status: int = 200) -> None:
        super().__init__(model, status)

    def render(self) -> WebResponse:
        response = WebResponse(self.status)
        response.headers["Content-Type"] = "application/json"
        response.data = json.dumps(self.model).encode()
        return response
