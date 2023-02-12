import json

from stage import Stage
from api import convert
from stage.base import Board
from stage.manual import ManualStage
from stage.wallclock import WallclockStage
from .storage import LineStorage


class TimelineItem:
    start: int
    duration: int
    screentime: int
    stage: Stage

    def __str__(self) -> str:
        return "{} {}".format(self.screentime, self.stage)

    def to_dict(self) -> dict:
        return {
            "start": convert.time_to_string(self.start),
            "duration": self.duration,
            "screentime": self.screentime,
            "stage": self.stage.to_dict()
        }

    @staticmethod
    def from_dict(board: Board, data: dict):
        item = TimelineItem()
        item.start = convert.string_to_time(data["start"])
        item.duration = data["duration"]
        item.screentime = data["screentime"]

        stage = data["stage"]
        if stage["name"] == "manual":
            item.stage = ManualStage.from_dict(board, stage)  # type: ignore
        elif stage["name"] == "wallclock":
            item.stage = WallclockStage.from_dict(board, stage)  # type: ignore
        else:
            item.stage = Stage()

        return item


class Timeline:
    _storage = LineStorage("data/timeline.txt")

    @staticmethod
    def load_dicts():
        for i, item in Timeline._storage.load():
            yield i, json.loads(item)

    @staticmethod
    def load_items(board: Board):
        for i, item in Timeline.load_dicts():
            yield i, TimelineItem.from_dict(board, item)

    @staticmethod
    def add(item: dict) -> int:
        return Timeline._storage.add(json.dumps(item).encode())

    @staticmethod
    def remove(id: int) -> bool:
        return Timeline._storage.remove(id)
