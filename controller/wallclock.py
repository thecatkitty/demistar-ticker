import json
import time

from config import *
from http import HttpRequest, HttpResponse
from view import ErrorView, JsonView

from machine import RTC


class WallclockController:
    dependencies = None

    def __init__(self) -> None:
        pass

    def get(self, request: HttpRequest) -> HttpResponse:
        print("api.wallclock: get")

        timestamp = time.localtime()
        return JsonView({
            "date": timestamp[:3],
            "time": timestamp[3:6]
        }).render()

    def post(self, request: HttpRequest) -> HttpResponse:
        print("api.wallclock: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        if type(data) is not dict:
            return ErrorView(422, "Payload is expected to be a dict").render()

        date = data.get("date")
        time = data.get("time")

        if type(date) is not list:
            return ErrorView(422, "'date' is expected to be a list").render()

        if type(time) is not list:
            return ErrorView(422, "'time' is expected to be a list").render()

        if len(date) != 3:
            return ErrorView(422, "'date' length is expected to be 3").render()

        if len(time) != 3:
            return ErrorView(422, "'time' length is expected to be 3").render()

        print(
            "api.wallclock: {:04}-{:02}-{:02} {:02}:{:02}:{:02}".format(*date, *time))
        RTC().datetime((date[0], date[1], date[2],
                        0, time[0], time[1], time[2], 0))
        return JsonView({}).render()
