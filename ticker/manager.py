from stage import Stage


class StageManager:
    _current: Stage

    def __init__(self) -> None:
        self._current = Stage()

    def handle(self) -> None:
        self._current.update()

    def set_stage(self, stage: Stage):
        if stage == self._current:
            pass

        self._current = stage
        self._current.show()
