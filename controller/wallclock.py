import json
import utime

from api import ErrorResponse, JsonResponse, convert
from config import *
from web import WebRequest, WebResponse

from machine import RTC


class WallclockController:
    dependencies = None

    def __init__(self) -> None:
        pass

    def get(self, request: WebRequest) -> WebResponse:
        print("api.wallclock: get")

        return JsonResponse({
            "time": convert.time_to_string(utime.time())
        })

    def post(self, request: WebRequest) -> WebResponse:
        print("api.wallclock: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorResponse(422, str(ve))

        if type(data) is not dict:
            return ErrorResponse(422, "Payload is expected to be a dict")

        time = data.get("time")

        if type(time) is not str:
            return ErrorResponse(422, "'time' is expected to be a string")

        try:
            timestamp = convert.string_to_time(time)
            year, month, mday, hour, minute, second, _, _ = utime.localtime(
                timestamp)

            print("api.wallclock: {}".format(time))
            RTC().datetime((year, month, mday, 0, hour, minute, second, 0))
        except ValueError as ve:
            return ErrorResponse(422, str(ve))

        return JsonResponse({})
