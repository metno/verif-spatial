import numpy as np
import pandas as pd
import xarray as xr


def time_to_unix(time):
    """Convert string/date time object(s) to
    unix time
    """
    time = np.atleast_1d(time)
    time_unix = []
    for _time in time:
        if _time is None:
            time_unix.append(None)
            continue
        if isinstance(_time, str | xr.DataArray):
            _time = pd.Timestamp(_time)
        time_unix.append(_time.strftime('%s'))
    return time_unix[0] if len(time_unix) == 1 else time_unix


def time_to_datetime(time):
    """Convert string/date time object(s) to
    unix time
    """
    time = np.atleast_1d(time)
    time_datetime = []
    for _time in time:
        if _time is None:
            time_datetime.append(None)
            continue
        if isinstance(_time, str):
            _time = pd.Timestamp(_time)
        if isinstance(_time, xr.DataArray):
            print('time:', _time)
            _time = pd.Timestamp(_time.item())
        time_datetime.append(_time)
    return time_datetime[0] if len(time_datetime) == 1 else time_datetime

