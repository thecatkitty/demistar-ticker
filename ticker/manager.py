from stage import Stage


class StageManager:
    _current: Stage

    def __init__(self) -> None:
        self._current = Stage()

    def handle(self) -> None:
        self._current.update()

    def set_stage(self, stage: Stage):
        self._current = stage
