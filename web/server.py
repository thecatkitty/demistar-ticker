import re
import socket
from collections import OrderedDict

from .definitions import STATUS_CODES

import web


RECV_BUFFER = 512
HTTP_METHOD_MAX_LENGTH = max([len(method) for method in web.METHODS])
HTTP_ENTITY_MAX_LENGTH = 16 * 1024


class WebServer:
    _local: socket.socket
    _remote: socket.socket
    _port: int
    _state: int
    _buff: bytearray

    _request: web.WebRequest
    _response: web.WebResponse

    _providers: OrderedDict
    _fallback: web.ContentProvider

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

        self._providers = OrderedDict()
        self._fallback = web.ContentProvider()

        print("web: listening at {}".format(port))

    @property
    def port(self) -> int:
        return self._port

    def add_provider(self, pattern: str, provider: web.ContentProvider):
        self._providers[pattern] = provider

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
            if reqline[0] not in [method[:len(reqline[0])] for method in web.METHODS]:
                print("web: invalid request line")
                return self._bad_request()

            if len(reqline) > 1:
                self._request = web.WebRequest(reqline[0])
                self._response = web.WebResponse()
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
            print("web: {method} {uri}".format(
                method=self._request.method, uri=self._request.uri))

        elif self._state == WebServer.STATE_REQLINE_COMPLETE:
            if b"\r\n\r\n" not in self._buff:
                self._try_receive()
                return

            headers_len = self._buff.index(b"\r\n\r\n")
            headers = self._buff[:headers_len].decode().split("\r\n")
            self._buff = self._buff[(headers_len + 4):]

            self._request.headers = {header[0]: header[1] for header in [
                header.split(": ", 1) for header in headers]}
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
            print("web: received {length} octets".format(
                length=len(self._request.data)))

        elif self._state == WebServer.STATE_RESPONDING:
            if self._response.code == 0:
                self._prepare_response()

            self._remote.write("HTTP/1.1 {code} {status}\r\n".format(
                code=self._response.code,
                status=STATUS_CODES[self._response.code]).encode())

            for name, value in self._response.headers.items():
                self._remote.write("{}: {}\r\n".format(name, value).encode())

            self._remote.write("\r\n".encode())

            for block in self._response.get_bytes():
                self._remote.write(block)

            self._remote.close()
            self._state = WebServer.STATE_IDLE
            print("web: responded with {}".format(
                web.STATUS_CODES[self._response.code]))

    def _try_receive(self) -> bool:
        try:
            data = self._remote.recv(RECV_BUFFER)
            self._remote.settimeout(0.5)
            self._buff.extend(data)
            return True

        except OSError as ose:
            print("web: connection closed ({})".format(ose.errno))
            self._state = WebServer.STATE_IDLE
            self._remote.close()
            return False

    def _prepare_response(self) -> None:
        if len(self._providers) == 0:
            self._response = web.WebResponse(500)
            print("web: no registered providers")
            return

        try:
            for pattern, provider in self._providers.items():
                if re.match(pattern, self._request.uri):
                    self._response = provider.handle_request(self._request)
                    return
        except Exception as e:
            self._response = web.WebResponse(500)
            self._response.headers["Content-Type"] = "text/plain"
            self._response.data = "{}: {}".format(type(e).__name__, e).encode()
            return

        self._response = self._fallback.handle_request(self._request)

    def _bad_request(self) -> None:
        self._response.code = 400
        self._state = WebServer.STATE_RESPONDING

    def _request_entity_too_large(self) -> None:
        self._response.code = 413
        self._state = WebServer.STATE_RESPONDING
