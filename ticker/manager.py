import utime

from stage import Stage


class StageManager:
    stages: list[tuple[int, Stage]] # screentime, stage
    _index: int
    _cycle_start: int

    def __init__(self) -> None:
        self.stages = list()
        self._cycle_start = 0

    def handle(self) -> None:
        if len(self.stages) == 0:
            return

        now = utime.time()
        if now > self._cycle_start + sum(screentime for screentime, _ in self.stages):
            self._index = 0
            self._cycle_start = now

            print("manager: switching to stage 0 - {} {}".format(*self.stages[0]))
            self.stages[0][1].show()
            return

        if now > self._cycle_start + sum(screentime for screentime, _ in self.stages[:self._index + 1]):
            self._index += 1
            if self._index >= len(self.stages):
                self._index = 0

            print("manager: switching to stage {} - {} {}".format(self._index, *self.stages[self._index]))
            self.stages[self._index][1].show()
            return

        self.stages[self._index][1].update()
