import json

MATRIXA_SPI = 1
MATRIXA_SCK = 14
MATRIXA_MOSI = 15
MATRIXA_CS = 13

MATRIXB_SPI = 0
MATRIXB_SCK = 18
MATRIXB_MOSI = 19
MATRIXB_CS = 17

RING_PIXELS = 16
RINGS = 2
RINGS_PIN = 9

LOCAL = dict()
with open('demistar.conf', 'r') as file:
    LOCAL = json.load(file)
