import network
import time

from neopixel import Neopixel

import config


# Static data
WHEEL = [
    (0xFF, 0x00, 0x00), (0xFF, 0x55, 0x00), (0xFF, 0xAA, 0x00),
    (0xFF, 0xFF, 0x00), (0xAA, 0xFF, 0x00), (0x55, 0xFF, 0x00),
    (0x00, 0xFF, 0x00), (0x00, 0xFF, 0x55), (0x00, 0xAA, 0xAA),
    (0x00, 0x55, 0xFF), (0x00, 0x00, 0xFF), (0x00, 0x00, 0xFF),
    (0x00, 0x00, 0xFF), (0x55, 0x00, 0xFF), (0xAA, 0x00, 0xFF),
    (0xFF, 0x00, 0xFF)
]


# Initialize the network interface
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect(config.IF_SSID, config.IF_PSK)

for i in range(config.IF_TRY):
    if net.status() < 0 or net.status() >= 3:
        break

    print("trying to connect...")
    time.sleep_ms(500)

if net.status() != 3:
    raise RuntimeError('connection failed')
else:
    print("connected to {ssid}, ipaddr = {addr}".format(
        ssid = net.config('ssid'),
        addr = net.ifconfig()[0]))


# Initialize LED rings
rings = Neopixel(config.RING_PIXELS * config.RINGS, 0, 11, "GRB")

index = 0

for pixel in WHEEL:
    rings.set_pixel(index, (pixel[0] >> 1, pixel[1] >> 1, pixel[2] >> 1))
    index = index + 1

for pixel in WHEEL:
    rings.set_pixel(index, (pixel[0] >> 2, pixel[1] >> 2, pixel[2] >> 2))
    index = index + 1


# Main program loop
while True:
    rings.show()
    time.sleep(1)
