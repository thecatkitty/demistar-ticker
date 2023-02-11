import os


class WebResponse:
    code: int
    headers: dict
    data: bytes

    def __init__(self, code: int = 0) -> None:
        self.code = code
        self.headers = dict()
        self.headers["Server"] = "demistar/0.1 (MicroPython {})".format(
            os.uname()[2])
        self.data = bytes(0)

    def get_bytes(self):
        offset = 0

        while offset < len(self.data):
            yield self.data[offset:(offset + 512)]
            offset += 512
