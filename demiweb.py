import socket

import http

RECV_BUFFER = 512
HTTP_METHOD_MAX_LENGTH = max([len(method) for method in http.METHODS])
HTTP_ENTITY_MAX_LENGTH = 16 * 1024

class HttpRequest:
    method: str
    uri: str
    headers: dict
    data: bytearray

    def __init__(self, method: str) -> None:
        self.method = method


class HttpResponse:
    code: int
    headers: dict
    data: bytes

    def __init__(self, code: int = 0) -> None:
        self.code = code
        self.headers = dict()
        self.data = bytes(0)

    def to_bytes(self) -> bytes:
        reqline = "HTTP/1.1 {code} {status}\r\n".format(
            code=self.code,
            status=http.STATUS_CODES[self.code])
        headers = "\r\n".join([
            "{}: {}".format(name, value) for name, value in self.headers.items()
        ])

        return reqline.encode() + headers.encode() + b"\r\n\r\n" + self.data


class WebServer:
    _local: socket.socket
    _remote: socket.socket
    _port: int
    _state: int
    _buff: bytearray
    _request: HttpRequest
    _response: HttpResponse

    STATE_IDLE = 0
    STATE_CONNECTED = 1
    STATE_METHOD_KNOWN = 2
    STATE_REQLINE_COMPLETE = 3
    STATE_READING_DATA = 4
    STATE_RESPONDING = 5

    def __init__(self, port: int = 80, backlog = 1) -> None:
        addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        self._local = socket.socket()
        self._local.bind(addr)
        self._local.setblocking(False)
        self._local.listen(backlog)
        
        self._port = port
        self._state = WebServer.STATE_IDLE

    @property
    def port(self) -> int:
        return self._port

    def handle(self) -> None:
        if self._state == WebServer.STATE_IDLE:
            try:
                self._remote, addr = self._local.accept()
                self._remote.settimeout(2)
            except OSError:
                return

            print("web: remote host connected from {addr}:{port}".format(
                addr=addr[0],
                port=addr[1]))
            self._state = WebServer.STATE_CONNECTED
            self._buff = bytearray()

        elif self._state == WebServer.STATE_CONNECTED:
            if not self._try_receive():
                return

            reqline = self._buff.decode().split()
            if reqline[0] not in [method[:len(reqline[0])] for method in http.METHODS]:
                print("web: invalid request line")
                return self._bad_request()

            if len(reqline) > 1:
                self._request = HttpRequest(reqline[0])
                self._response = HttpResponse()
                self._buff = self._buff[(len(reqline[0]) + 1):]
                self._state = WebServer.STATE_METHOD_KNOWN

        elif self._state == WebServer.STATE_METHOD_KNOWN:
            if b"\r\n" not in self._buff:
                if b"\n" in self._buff or (b"\r" in self._buff and self._buff[-1] != ord(b"\r")):
                    print("web: unexpected character in the request line")
                    return self._bad_request()

                self._try_receive()
                return

            reqline = self._buff.decode().split("\r\n", 1)[0]
            self._buff = self._buff[(len(reqline) + 2):]
            
            reqline = reqline.split()
            if len(reqline) != 2:
                print("web: wrong number of parts in the request line")
                return self._bad_request()

            if not reqline[1].startswith("HTTP/1."):
                print("web: wrong protocol version in the request line")
                return self._bad_request()

            self._request.uri = reqline[0]
            self._state = WebServer.STATE_REQLINE_COMPLETE
            print("web: {method} {uri}".format(method=self._request.method, uri=self._request.uri))

        elif self._state == WebServer.STATE_REQLINE_COMPLETE:
            if b"\r\n\r\n" not in self._buff:
                self._try_receive()
                return

            headers_len = self._buff.index(b"\r\n\r\n")
            headers = self._buff[:headers_len].decode().split("\r\n")
            self._buff = self._buff[(headers_len + 4):]

            self._request.headers = {header[0]: header[1] for header in [header.split(": ", 1) for header in headers]}
            if "Content-Length" in self._request.headers.keys():
                data_length = int(self._request.headers["Content-Length"])
                if data_length > HTTP_ENTITY_MAX_LENGTH:
                    return self._request_entity_too_large()
                else:
                    self._request.data = bytearray(data_length)
                    self._state = WebServer.STATE_READING_DATA
            else:
                self._state = WebServer.STATE_RESPONDING

        elif self._state == WebServer.STATE_READING_DATA:
            data_length = int(self._request.headers["Content-Length"])
            if len(self._buff) < data_length:
                self._try_receive()
                return

            self._request.data[:] = self._buff[:data_length]
            self._state = WebServer.STATE_RESPONDING
            print("web: received {length} octets".format(length=len(self._request.data)))

        elif self._state == WebServer.STATE_RESPONDING:
            if self._response.code == 0:
                self._response.code = 200
                self._response.headers["Content-Type"] = "text/html"
                self._response.data = "<h1>It works!</h1>".encode()

            self._remote.write(self._response.to_bytes())
            self._remote.close()
            self._state = WebServer.STATE_IDLE
            print("web: responded with {}".format(http.STATUS_CODES[self._response.code]))

    def _try_receive(self) -> bool:
        try:
            data = self._remote.recv(RECV_BUFFER)
            self._remote.settimeout(0.5)
            self._buff.extend(data)
            return True

        except OSError as ose:
            print("web: connection closed ({reason})".format(reason=ose.strerror))
            self._state = WebServer.STATE_IDLE
            self._remote.close()
            return False

    def _bad_request(self) -> None:
        self._response.code = 400
        self._state = WebServer.STATE_RESPONDING

    def _request_entity_too_large(self) -> None:
        self._response.code = 413
        self._state = WebServer.STATE_RESPONDING
