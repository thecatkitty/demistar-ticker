from config import *
from ticker import DemistarTicker


app = DemistarTicker()
app.init_rings(RING_PIXELS * RINGS, RINGS_PIN)
app.init_matrix(0, MATRIXA_SPI, MATRIXA_SCK, MATRIXA_MOSI, MATRIXA_CS)
app.init_matrix(1, MATRIXB_SPI, MATRIXB_SCK, MATRIXB_MOSI, MATRIXB_CS)

app.get_matrix(0).draw_text("Demistar")
app.get_matrix(0).update()

if not app.init_network(IF_SSID, IF_PSK, IF_TRY):
    print("connection failed")
    app.get_ring(1).fill(64, 0, 0)
    app.get_matrix(1).draw_text("no connection")
else:
    print("connected")

    app.get_ring(1).fill(0, 64, 0)
    addr = app.init_server(2137)
    print("listening at {}".format(addr))
    app.get_matrix(1).draw_text(addr.split(":")[0])

app.get_matrix(1).update()

app.rings_changed()
app.run()
