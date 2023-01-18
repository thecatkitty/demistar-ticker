from api import JsonView
from http import HttpRequest, HttpResponse

from ticker.manager import StageManager, TimelineItem


class TimelineController:
    dependencies = ["stage_manager"]

    _manager: StageManager

    def __init__(self, stage_manager: StageManager) -> None:
        self._manager = stage_manager

    def get(self, request: HttpRequest) -> HttpResponse:
        print("api.timeline: get")
        return JsonView({
            "backlog": [item.to_dict() for item in self._manager.timeline],
            "cycle": [item.to_dict() for item in self._manager.cycle]
        }).render()

    def post(self, request: HttpRequest) -> HttpResponse:
        return JsonView({}).render()
