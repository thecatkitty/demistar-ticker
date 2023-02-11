from .json import JsonResponse


class ErrorResponse(JsonResponse):
    def __init__(self, status: int, message: str) -> None:
        super().__init__({
            "error": message
        }, status)
