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
    _uri: str

    STATE_IDLE = 0
    STATE_CONNECTED = 1
    STATE_METHOD_KNOWN = 2
    STATE_REQLINE_COMPLETE = 3

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
            if reqline[0] not in [method[:len(reqline[0])] for method in HTTP_METHODS]:
                print("web: invalid request line")
                return self._bad_request()

            if len(reqline) > 1:
                self._method = reqline[0]
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

            self._uri = reqline[0]
            self._state = WebServer.STATE_REQLINE_COMPLETE
            print("web: {method} {uri}".format(method=self._method, uri=self._uri))

        elif self._state == WebServer.STATE_REQLINE_COMPLETE:
            self._remote.send("HTTP/1.1 200 OK\r\nContent-Type: text/html\r\n\r\n<h1>It Works!</h1><p>owo</p>")
            self._remote.close()
            self._state = WebServer.STATE_IDLE
            print("web: response sent and connection closed")

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
        self._remote.send("HTTP/1.1 400 Bad Request\r\n\r\n")
        self._remote.close()
        self._state = WebServer.STATE_IDLE
        print("web: bad request, connection closed")
