import utime

from stage import Stage


class TimelineItem:
    start: int
    duration: int
    screentime: int
    stage: Stage

    def __str__(self) -> str:
        return "{} {}".format(self.screentime, self.stage)

    def to_dict(self) -> dict:
        return {
            "start": self.start,
            "duration": self.duration,
            "screentime": self.screentime,
            "stage": self.stage.to_dict()
        }


class StageManager:
    timeline: list[TimelineItem]
    cycle: list[TimelineItem]
    _index: int
    _cycle_start: int

    def __init__(self) -> None:
        self.timeline = list()
        self.cycle = list()
        self._index = 0
        self._cycle_start = 0

    def _get_cycle(self, now: int) -> None:
        fresh = list(item for item in self.timeline if item.start < now)
        for item in fresh:
            print("manager: in - {}".format(item))
            self.timeline.remove(item)
            self.cycle.append(item)

        stale = list(item for item in self.cycle
                     if item.duration > 0 and item.start + item.duration < now)
        for item in stale:
            print("manager: out - {}".format(item))
            self.cycle.remove(item)

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
        now = utime.time()
        self._get_cycle(now)

        if len(self.cycle) == 0:
            return

        if self._cycle_start == 0 or self._index >= len(self.cycle):
            return self._restart_cycle(now)

        if now > self._cycle_start + sum(item.screentime for item in self.cycle[:self._index + 1]):
            return self._next_stage()

        self.cycle[self._index].stage.update()

    def add_stage(self, screentime: int, stage: Stage, start: int = 0, duration: int = 0) -> None:
        item = TimelineItem()
        item.start = utime.time() if start == 0 else start
        item.duration = duration
        item.screentime = screentime
        item.stage = stage
        self.timeline.append(item)
