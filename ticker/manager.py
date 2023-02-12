import utime

from api import convert
from stage import Stage
from stage.base import Board
from .timeline import Timeline, TimelineItem


class StageManager:
    cycle: list[tuple[int, TimelineItem]]
    _index: int
    _cycle_start: int
    _board: Board

    def __init__(self, board: Board) -> None:
        self.cycle = list()
        self._index = 0
        self._cycle_start = 0
        self._board = board

    def _get_cycle(self, now: int) -> None:
        cycle_ids = list(id for id, _ in self.cycle)
        fresh = list((id, item) for id, item in Timeline.load_items()
                     if item.start < now and id not in cycle_ids)
        for id, item in fresh:
            print("manager: in - {} {}".format(id, item))
            self.cycle.append((id, item))

        stale = list(id for id, item in self.cycle
                     if item.duration > 0 and item.start + item.duration < now)
        for id in stale:
            item = next(i for i in self.cycle if i[0] == id)
            print("manager: out - {} {}".format(*item))
            self.cycle.remove(item)
            Timeline.remove(id)

    def _set_stage(self, index: int) -> None:
        self._index = index
        print("manager: stage {} - {} {}".format(index, *self.cycle[index]))
        (self.cycle[index])[1].stage.show(self._board)

    def _restart_cycle(self, now: int) -> None:
        self._cycle_start = now
        self._set_stage(0)

    def _next_stage(self) -> None:
        self._index += 1
        if self._index >= len(self.cycle):
            print("manager: cycle {} end".format(
                convert.time_to_string(self._cycle_start)))
            return

        self._set_stage(self._index)

    def handle(self) -> None:
        now = utime.time()
        self._get_cycle(now)

        if len(self.cycle) == 0:
            return

        if self._cycle_start == 0 or self._index >= len(self.cycle):
            return self._restart_cycle(now)

        if now > self._cycle_start + sum(item.screentime for _, item in self.cycle[:self._index + 1]):
            return self._next_stage()

        self.cycle[self._index][1].stage.update(self._board)

    def add_stage(self, screentime: int, stage: Stage, start: int = 0, duration: int = 0) -> int:
        item = TimelineItem()
        item.start = utime.time() if start == 0 else start
        item.duration = duration
        item.screentime = screentime
        item.stage = stage
        return Timeline.add(item.to_dict())

    def remove(self, id: int):
        if id in [cid for cid, _ in self.cycle]:
            item = next(i for i in self.cycle if i[0] == id)
            self.cycle.remove(item)
            self._restart_cycle(utime.time())

        Timeline.remove(id)
