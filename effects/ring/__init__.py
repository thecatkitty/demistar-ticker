from ticker.ring import Ring
from .base import RingEffect
from .blink import Blink
from .breath import Breath

registry = {
    "blink": Blink,
    "breath": Breath
}


def create(ring: Ring, name: str, args: tuple, time_ms: int) -> RingEffect:
    if name not in registry.keys():
        return None  # type: ignore

    return registry[name](ring, args, time_ms)
