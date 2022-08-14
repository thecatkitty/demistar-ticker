import config
from demistar import Demistar


app = Demistar()

if not app.init_network(config.IF_SSID, config.IF_PSK, config.IF_TRY):
    print("connection failed")
else:
    print("connected")

    addr = app.init_server(2137)
    print("listening at {addr}".format(addr = addr))

app.init_rings(config.RING_PIXELS * config.RINGS, config.RINGS_PIN)

app.run()
