import network
import ntptime
import time

from config import *
from ticker import DemistarTicker, MatrixDisplay, Ring

from machine import RTC, reset
from driver.neopixel import Neopixel


# Definition of components
top_display = MatrixDisplay(MATRIXA_SPI, MATRIXA_SCK, MATRIXA_MOSI, MATRIXA_CS)
bottom_display = MatrixDisplay(
    MATRIXB_SPI, MATRIXB_SCK, MATRIXB_MOSI, MATRIXB_CS)

strip = Neopixel(RING_PIXELS * RINGS, 0, RINGS_PIN, "GRB", delay=0.001)
outer_ring = Ring(strip, 0, 16)
inner_ring = Ring(strip, 16, 16)

app = DemistarTicker(top_display, bottom_display, inner_ring, outer_ring)

# Initialization
strip.clear()
strip.show()

top_display.draw_text("Demistar Ticker")
top_display.update()

# Going online
net = network.WLAN(network.STA_IF)
net.active(True)
net.connect(IF_SSID, IF_PSK)

for i in range(IF_TRY):
    if net.status() < 0 or net.status() >= 3:
        break

    print("net: connecting ({}/{})".format(i + 1, IF_TRY))
    inner_ring[i] = 0, 0, 64
    time.sleep(1)

if net.status() != 3:
    print("net: connection failed")
    inner_ring.fill(64, 0, 0)
    bottom_display.draw_text("no connection")
    bottom_display.update()

    time.sleep(15)
    reset()

# We're connected!
print("net: address {}".format(net.ifconfig()[0]))
inner_ring.fill(0, 64, 0)

ntptime.settime()
timestamp = time.localtime(time.time() + TZ_OFFSET)
RTC().datetime((timestamp[0], timestamp[1], timestamp[2],
                0, timestamp[3], timestamp[4], timestamp[5], 0))

app.run(2137)
