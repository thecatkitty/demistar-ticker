import io
import os


class LineStorage:
    _file: io.BufferedRandom
    _last: int
    _lock: bool

    def __init__(self, filename: str) -> None:
        try:
            os.stat(filename)
        except OSError:
            with open(filename, 'w') as _:
                pass

        self._file = open(filename, "r+b")
        self._last = self._count_all() - 1
        self._lock = False

    def _count_all(self) -> int:
        i = 0
        self._file.seek(0)

        while True:
            line = self._file.readline()
            if len(line) == 0:
                break

            i += 1

        return i

    def load(self):
        if not self.acquire():
            return None

        i = -1
        self._file.seek(0)

        while True:
            line = self._file.readline()
            if len(line) == 0:
                break

            i += 1
            if line[0] == ord(b'-'):
                continue

            yield i, line[1:]

        self.release()

    def add(self, line: bytes) -> int:
        if not self.acquire():
            return -1

        self._file.seek(0, 2)
        self._file.write(b'+')
        self._file.write(line)
        self._file.write(b'\n')
        self._file.flush()

        self.release()
        self._last += 1
        return self._last

    def remove(self, id: int) -> bool:
        if not self.acquire():
            return False

        i = 0
        self._file.seek(0)

        while True:
            if i == id:
                self._file.write(b'-')
                self._file.flush()
                break

            line = self._file.readline()
            if len(line) == 0:
                break

            i += 1

        self.release()
        return True

    def acquire(self) -> bool:
        if self._lock:
            return False

        self._lock = True
        return True

    def release(self):
        self._lock = False
