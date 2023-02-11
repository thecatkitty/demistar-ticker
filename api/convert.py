import json
import utime


def time_to_string(time: int) -> str:
    year, month, mday, hour, minute, second, _, _ = utime.localtime(time)
    return "{}-{:02}-{:02}T{:02}:{:02}:{:02}".format(
        year, month, mday, hour, minute, second)


def string_to_time(string: str) -> int:
    parts = string.split("T")
    if len(parts) != 2:
        raise ValueError("time missing")

    date, time = parts

    date_parts = date.split("-")
    if len(date_parts) != 3:
        raise ValueError("date incomplete")

    time_parts = time.split(":")
    if len(time_parts) != 3:
        raise ValueError("time incomplete")

    year, month, mday = date_parts
    hour, minute, second = time_parts
    return utime.mktime((int(year), int(month), int(mday), int(hour), int(minute), int(second), 0, 0))


def to_json_bytes(node: object):
    if type(node) is dict:
        yield "{".encode()

        for i, item in enumerate(node.items()):
            if i != 0:
                yield ",".encode()

            key, value = item
            yield (json.dumps(str(key)) + ":").encode()

            for chunk in to_json_bytes(value):
                yield chunk

        yield "}".encode()

    elif type(node) is list:
        yield "[".encode()

        for i, item in enumerate(node):
            if i != 0:
                yield ",".encode()

            for chunk in to_json_bytes(item):
                yield chunk

        yield "]".encode()

    else:
        yield json.dumps(node).encode()
