# Read NetCDF file using xarray. The NetCDF files should be
# compatible with bris-inference, with the following shapes:
#
# ...

import numpy as np
import xarray as xr
import pandas as pd
from .datareader import DataReader
from .utils import time_to_datetime


class NetCDFReader(DataReader):
    """
    """
    def __init__(
        self,
        path,
    ) -> None:
        #super
        self.ds = xr.open_dataset(path)
        self.reference_time = time_to_datetime(self.ds.forecast_reference_time)
        self.lead_times = time_to_datetime(self.ds.time)
