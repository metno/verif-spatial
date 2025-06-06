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
    )
        #super
        self.ds = xr.open_dataset(path)
        self.date = self.ds.date

    def read(self, date):
        """ """
        return self.ds
