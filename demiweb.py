import socket

RECV_BUFFER = 512
HTTP_METHODS = ["GET", "HEAD", "POST", "PUT", "DELETE", "CONNECT", "OPTIONS", "TRACE"]
HTTP_METHOD_MAX_LENGTH = max([len(method) for method in HTTP_METHODS])

class WebServer:
    _local: socket.socket
    _remote: socket.socket
    _port: int
    _state: int
    _buff: bytearray

    _method: str

    STATE_IDLE = 0
    STATE_CONNECTED = 1
    STATE_METHOD_KNOWN = 2

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
            try:
                data = self._remote.recv(RECV_BUFFER)
                if not data:
                    return
            except OSError:
                print("web: connection closed due to inactivity")
                self._state = WebServer.STATE_IDLE
                self._remote.close()
                return

            self._remote.settimeout(0.5)
            self._buff.extend(data)

            prolog = self._buff.decode().split()
            if prolog[0] not in [method[:len(prolog[0])] for method in HTTP_METHODS]:
                print("web: invalid request prolog")
                return self._bad_request()

            if len(prolog) > 1:
                self._method = prolog[0]
                self._buff = self._buff[(len(prolog[0]) + 1):]
                print("web: method = {method}".format(method=self._method))
                self._state = WebServer.STATE_METHOD_KNOWN

        elif self._state == WebServer.STATE_METHOD_KNOWN:
            self._remote.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>It Works!</h1><p>owo</p>")
            self._state = WebServer.STATE_IDLE
            self._remote.close()
            print("web: response sent and connection closed")

    def _bad_request(self) -> None:
        self._remote.send("HTTP/1.1 400 Bad Request\r\n\r\n")
        self._remote.close()
        self._state = WebServer.STATE_IDLE
