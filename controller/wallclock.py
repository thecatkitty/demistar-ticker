import json
import utime

from api import ErrorView, JsonView, convert
from config import *
from http import HttpRequest, HttpResponse

from machine import RTC


class WallclockController:
    dependencies = None

    def __init__(self) -> None:
        pass

    def get(self, request: HttpRequest) -> HttpResponse:
        print("api.wallclock: get")

        return JsonView({
            "time": convert.time_to_string(utime.time())
        }).render()

    def post(self, request: HttpRequest) -> HttpResponse:
        print("api.wallclock: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        if type(data) is not dict:
            return ErrorView(422, "Payload is expected to be a dict").render()

        time = data.get("time")

        if type(time) is not str:
            return ErrorView(422, "'time' is expected to be a string").render()

        try:
            timestamp = convert.string_to_time(time)
            year, month, mday, hour, minute, second, _, _ = utime.localtime(
                timestamp)

            print("api.wallclock: {}".format(time))
            RTC().datetime((year, month, mday, 0, hour, minute, second, 0))
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        return JsonView({}).render()
