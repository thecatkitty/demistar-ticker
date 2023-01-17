from .base import RingEffect
from .blink import Blink
from .breath import Breath

registry = {
    "blink": Blink,
    "breath": Breath
}
