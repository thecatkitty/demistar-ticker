import json
import utime

from api import ErrorResponse, JsonResponse, convert
from web import WebRequest, WebResponse

from ticker.manager import StageManager
from ticker.timeline import Timeline


class TimelineController:
    dependencies = ["stage_manager"]

    _manager: StageManager

    def __init__(self, stage_manager: StageManager) -> None:
        self._manager = stage_manager

    @staticmethod
    def _get_backlog():
        for id, item in Timeline.load_dicts():
            if type(item) is dict:
                item.update({"id": id})
                yield item

    def get(self, request: WebRequest) -> WebResponse:
        print("api.timeline: get")
        return JsonResponse({
            "backlog": TimelineController._get_backlog,
            "cycle": [id for id, _ in self._manager.cycle]
        })

    def post(self, request: WebRequest) -> WebResponse:
        print("api.timeline: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorResponse(422, str(ve))

        if type(data) is not dict:
            return ErrorResponse(422, "Payload is expected to be a dict")

        start = data.get("start")
        try:
            convert.string_to_time(start)  # type: ignore
        except Exception:
            data["start"] = convert.time_to_string(utime.time())

        duration = data.get("duration")
        if type(duration) is not int:
            data["duration"] = 0

        screentime = data.get("screentime")
        if type(screentime) is not int:
            return ErrorResponse(422, "'screentime' is expected to be an integer")

        stage = data.get("stage")
        if type(stage) is not dict:
            return ErrorResponse(422, "'stage' is expected to be an dict")

        stage_name = stage.get("name")
        if type(stage_name) is not str:
            return ErrorResponse(422, "'stage.name' is expected to be a string")

        if stage_name not in ["manual", "wallclock"]:
            return ErrorResponse(422, "unknown 'stage.name'")

        return JsonResponse({
            "id": Timeline.add(data)
        })
