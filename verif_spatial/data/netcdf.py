# Read NetCDF file using xarray. The NetCDF files should be
# compatible with bris-inference, with the following shapes:
#
# ...

import numpy as np
import xarray as xr
from .datareader import DataReader


class NetCDFReader(DataReader):
    """Need to read file in constructor to get the date
    from the metadata, in case a Zarr file is also provided
    """
    def __init__(
        self,
        path,
    ) -> None:
        #super
        self.ds = xr.open_dataset(path)
        self.date = "2022-01-01T00" #self.ds.date
        self.lead_times = [0,1,2,3,4,5,6,7,8,9] #self.ds.lead_times
