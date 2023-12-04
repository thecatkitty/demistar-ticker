import machine
import network
import time

from config import *
from ticker import DemistarTicker, MatrixDisplay, Ring
from stage import Board

from driver.neopixel import Neopixel


# Definition of components
top_display = MatrixDisplay(MATRIXA_SPI, MATRIXA_SCK, MATRIXA_MOSI, MATRIXA_CS)
bottom_display = MatrixDisplay(
    MATRIXB_SPI, MATRIXB_SCK, MATRIXB_MOSI, MATRIXB_CS)

strip = Neopixel(RING_PIXELS * RINGS, 0, RINGS_PIN, "GRB", delay=0.001)
outer_ring = Ring(strip, 0, 16)
inner_ring = Ring(strip, 16, 16)

board = Board(top_display, bottom_display, inner_ring, outer_ring)
app = DemistarTicker(board)

# Initialization
strip.clear()
strip.show()

top_display.draw_text("Demistar Ticker")
top_display.update()
bottom_display.clear()
bottom_display.update()

# Going online
net = network.WLAN(network.STA_IF)
net.active(True)
app.run(2137)
