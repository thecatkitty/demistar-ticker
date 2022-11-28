from machine import Pin, SPI

import config
from ticker import DemistarTicker


app = DemistarTicker()
app.init_rings(config.RING_PIXELS * config.RINGS, config.RINGS_PIN)
app.init_matrix(0, SPI(config.MATRIXA_SPI,
    sck=Pin(config.MATRIXA_SCK),
    mosi=Pin(config.MATRIXA_MOSI)), Pin(config.MATRIXA_CS))
app.init_matrix(1, SPI(config.MATRIXB_SPI,
    sck=Pin(config.MATRIXB_SCK),
    mosi=Pin(config.MATRIXB_MOSI)), Pin(config.MATRIXB_CS))

app.get_matrix(0).text('Demistar', 0, 0)
app.get_matrix(0).show()

if not app.init_network(config.IF_SSID, config.IF_PSK, config.IF_TRY):
    print("connection failed")
    app.get_ring(1).fill(64, 0, 0)
    app.get_matrix(1).text("no conn", 4, 0)
else:
    print("connected")

    app.get_ring(1).fill(0, 64, 0)
    addr = app.init_server(2137)
    print("listening at {}".format(addr))
    app.get_matrix(1).text(".{}".format(addr.split(".")[-1]), 0, 0)

app.get_matrix(1).show()

app.rings_changed()
app.run()
