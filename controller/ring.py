from neopixel import Neopixel


class RingsProviderInterface:
    def get_rings(self) -> Neopixel:
        raise NotImplementedError()

    def rings_changed(self) -> None:
        raise NotImplementedError()
