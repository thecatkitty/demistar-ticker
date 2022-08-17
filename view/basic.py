from http import HttpResponse

class BasicView:
    model: object
    status: int

    def __init__(self, model, status: int = 200) -> None:
        self.model = model
        self.status = status

    def render(self) -> HttpResponse:
        raise NotImplementedError()
