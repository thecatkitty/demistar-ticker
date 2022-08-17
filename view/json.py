import json

from http import HttpResponse
from .basic import BasicView

class JsonView(BasicView):
    def __init__(self, model, status: int = 200) -> None:
        super().__init__(model, status)

    def render(self) -> HttpResponse:
        response = HttpResponse(self.status)
        response.headers["Content-Type"] = "application/json"
        response.data = json.dumps(self.model).encode()
        return response
