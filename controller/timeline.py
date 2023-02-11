import json

from api import ErrorView, JsonView, convert
from web import WebRequest, WebResponse

from stage.base import Board
from stage.manual import ManualStage
from stage.wallclock import WallclockStage
from ticker.manager import StageManager


class TimelineController:
    dependencies = ["board", "stage_manager"]

    _board: Board
    _manager: StageManager

    def __init__(self, board: Board, stage_manager: StageManager) -> None:
        self._board = board
        self._manager = stage_manager

    def get(self, request: WebRequest) -> WebResponse:
        print("api.timeline: get")
        return JsonView({
            "backlog": [item.to_dict() for item in self._manager.timeline],
            "cycle": [item.to_dict() for item in self._manager.cycle]
        }).render()

    def post(self, request: WebRequest) -> WebResponse:
        print("api.timeline: post")
        try:
            data = json.loads(request.data.decode())
        except ValueError as ve:
            return ErrorView(422, str(ve)).render()

        if type(data) is not dict:
            return ErrorView(422, "Payload is expected to be a dict").render()

        start = data.get("start")
        try:
            start = convert.string_to_time(start)  # type: ignore
        except Exception:
            start = 0

        duration = data.get("duration")
        if type(duration) is not int:
            duration = 0

        screentime = data.get("screentime")
        if type(screentime) is not int:
            return ErrorView(422, "'screentime' is expected to be an integer").render()

        stage = data.get("stage")
        if type(stage) is not dict:
            return ErrorView(422, "'stage' is expected to be an dict").render()

        stage_name = stage.get("name")
        if type(stage_name) is not str:
            return ErrorView(422, "'stage.name' is expected to be a string").render()

        if stage_name == "manual":
            stage = ManualStage.from_dict(self._board, stage)  # type: ignore
        elif stage_name == "wallclock":
            stage = WallclockStage.from_dict(
                self._board, stage)  # type: ignore
        else:
            return ErrorView(422, "unknown 'stage.name'").render()

        self._manager.add_stage(screentime, stage, start,  # type: ignore
                                duration)
        return JsonView({}).render()
