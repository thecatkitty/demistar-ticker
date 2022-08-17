from .json import JsonView

class ErrorView(JsonView):
    def __init__(self, status: int, message: str) -> None:
        super().__init__({
            "error": message
        }, status)
