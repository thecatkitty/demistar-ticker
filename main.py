import config
from demistar import Demistar


app = Demistar()
app.init_rings(config.RING_PIXELS * config.RINGS, config.RINGS_PIN)

if not app.init_network(config.IF_SSID, config.IF_PSK, config.IF_TRY):
    print("connection failed")
    app.get_rings().set_pixel_line(16, 32, (64, 0, 0))
else:
    print("connected")

    app.get_rings().set_pixel_line(16, 32, (0, 64, 0))
    addr = app.init_server(2137)
    print("listening at {}".format(addr))

app.rings_changed()
app.run()
