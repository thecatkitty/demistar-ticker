class HttpRequest:
    method: str
    uri: str
    headers: dict
    data: bytearray

    def __init__(self, method: str) -> None:
        self.method = method
