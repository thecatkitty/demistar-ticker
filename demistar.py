import network
import socket
import time

from neopixel import Neopixel

WHEEL = [
    (0xFF, 0x00, 0x00), (0xFF, 0x55, 0x00), (0xFF, 0xAA, 0x00),
    (0xFF, 0xFF, 0x00), (0xAA, 0xFF, 0x00), (0x55, 0xFF, 0x00),
    (0x00, 0xFF, 0x00), (0x00, 0xFF, 0x55), (0x00, 0xAA, 0xAA),
    (0x00, 0x55, 0xFF), (0x00, 0x00, 0xFF), (0x00, 0x00, 0xFF),
    (0x00, 0x00, 0xFF), (0x55, 0x00, 0xFF), (0xAA, 0x00, 0xFF),
    (0xFF, 0x00, 0xFF)
]

class Demistar:
    _net: network.WLAN
    _rings: Neopixel
    _sock: socket.socket

    def init_network(self, ssid: str, psk: str, retries: int) -> bool:
        self._net = network.WLAN(network.STA_IF)
        self._net.active(True)
        self._net.connect(ssid, psk)

        for i in range(retries):
            if self._net.status() < 0 or self._net.status() >= 3:
                break

            print("trying to connect ({i}/{max})".format(
                i = i + 1,
                max = retries))
            time.sleep_ms(500)

        return self._net.status() == 3

    def init_rings(self, length: int, pin: int) -> None:
        self._rings = Neopixel(length, 0, pin, "GRB")

        index = 0
        for pixel in WHEEL:
            self._rings.set_pixel(index, (pixel[0] >> 1, pixel[1] >> 1, pixel[2] >> 1))
            index = index + 1

        for pixel in WHEEL:
            self._rings.set_pixel(index, (pixel[0] >> 2, pixel[1] >> 2, pixel[2] >> 2))
            index = index + 1

    def init_server(self, port: int) -> str:
        addr = socket.getaddrinfo("0.0.0.0", port)[0][-1]
        self._sock = socket.socket()
        self._sock.bind(addr)
        self._sock.setblocking(False)
        self._sock.listen(1)
        return "{host}:{port}".format(host = self._net.ifconfig()[0], port = port)

    def run(self) -> None:
        while True:
            self._loop()

    def _loop(self) -> None:
        self._rings.show()
        try:
            client, addr = self._sock.accept()
            client.settimeout(2)
            print("client connected from {addr}:{port}".format(
                addr = addr[0],
                port = addr[1]))

            try:
                request = client.recv(1024)
                print(request)

                client.send("received bytes: {bytes}\n".format(bytes = len(request)))
                client.close()
                print("connection with {addr}:{port} closed\n".format(
                    addr = addr[0],
                    port = addr[1]))

            except OSError as ose:
                client.close()
                print("connection with {addr}:{port} broken\n".format(
                    addr = addr[0],
                    port = addr[1]))
            
        except OSError as ose:
            time.sleep_ms(125)
