from api import JsonResponse
from config import *
from effects import display as dfx
from effects import ring as rfx
from web import WebRequest, WebResponse


class EffectsController:
    dependencies = None

    def __init__(self) -> None:
        pass

    def get(self, request: WebRequest) -> WebResponse:
        print("api.effects: get")

        return JsonResponse({
            "display": [key for key in dfx.registry.keys()],
            "ring": [key for key in rfx.registry.keys()]
        })
