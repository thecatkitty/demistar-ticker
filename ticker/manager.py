import utime

from stage import Stage


class TimelineItem:
    start: int
    duration: int
    screentime: int
    stage: Stage

    def __str__(self) -> str:
        return "{} {}".format(self.screentime, self.stage)


class StageManager:
    cycle: list[TimelineItem]
    _index: int
    _cycle_start: int

    def __init__(self) -> None:
        self.cycle = list()
        self._index = 0
        self._cycle_start = 0

    def _set_stage(self, index: int) -> None:
        self._index = index
        print("manager: stage {} - {}".format(index, self.cycle[index]))
        self.cycle[index].stage.show()

    def _restart_cycle(self, now: int) -> None:
        self._cycle_start = now
        self._set_stage(0)

    def _next_stage(self) -> None:
        self._index += 1
        if self._index >= len(self.cycle):
            print("manager: cycle {} end".format(self._cycle_start))
            return

        self._set_stage(self._index)

    def handle(self) -> None:
        if len(self.cycle) == 0:
            return

        now = utime.time()
        if self._cycle_start == 0 or self._index >= len(self.cycle):
            return self._restart_cycle(now)

        if now > self._cycle_start + sum(item.screentime for item in self.cycle[:self._index + 1]):
            return self._next_stage()

        self.cycle[self._index].stage.update()

    def add_stage(self, screentime: int, stage: Stage) -> None:
        item = TimelineItem()
        item.screentime = screentime
        item.stage = stage
        self.cycle.append(item)
