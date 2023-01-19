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
