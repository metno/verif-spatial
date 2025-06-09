import pandas as pd

def time_to_unix(*time):
    """Convert string/date time object(s) to
    unix time
    """
    time_unix = []
    for _time in time:
        if _time is None:
            time_unix.append(None)
            continue
        if isinstance(_time, str):
            _time = pd.Timestamp(_time)
        time_unix.append(_time.strftime('%s'))
    return time_unix[0] if len(time_unix) == 1 else time_unix


def time_to_datetime(*time):
    """Convert string/date time object(s) to
    unix time
    """
    time_unix = []
    for _time in time:
        if _time is None:
            time_unix.append(None)
            continue
        if isinstance(_time, str):
            _time = pd.Timestamp(_time)
        time_unix.append(_time)
    return time_unix[0] if len(time_unix) == 1 else time_unix

