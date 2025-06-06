import numpy as np
from anemoi.datasets import open_dataset

from .convert import convert
from .datareader import DataReader


class ZarrReader(DataReader):
    def __init__(
        self,
        path,
        **kwargs,
    ) -> None:
        self.kwargs = kwargs
        #super

    def read(self, date):
        """Convert from anemoi datasets to xarray """
        ds = open_dataset(self.path)
        data = ds[date]

        # convert variables
        # name to index ...
