import os

from .definitions import STATUS_CODES


class HttpResponse:
    code: int
    headers: dict
    data: bytes

    def __init__(self, code: int = 0) -> None:
        self.code = code
        self.headers = dict()
        self.headers["Server"] = "demistar/0.1 (MicroPython {})".format(
            os.uname()[2])
        self.data = bytes(0)

    def to_bytes(self) -> bytes:
        reqline = "HTTP/1.1 {code} {status}\r\n".format(
            code=self.code,
            status=STATUS_CODES[self.code])
        headers = "\r\n".join([
            "{}: {}".format(name, value) for name, value in self.headers.items()
        ])

        return reqline.encode() + headers.encode() + b"\r\n\r\n" + self.data
