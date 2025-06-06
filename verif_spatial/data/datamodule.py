import numpy as np
from .netcdf import NetCDFReader
from .zarr import ZarrReader

class DataModule:
    def __init__(
        self,
        paths: str or list[str] = None,
        interp_res: float = None
        date: str = None,
    ) -> None:
    
    paths = np.atleast_1d(paths)

    # first go through metadata
    self.data_objs = []
    self.dates = []
    for path in paths:
        suffix = paths.split('.')[-1]
        if suffix == 'nc':
            data_obj = NetCDFReader(path)
            self.dates.append(data_obj.date)
        elif suffix == 'zarr':
            data_obj = ZarrReader(path)
        else:
            raise NotImplementedError("Only NetCDF and Zarr formats are currently supported")
        self.data_objs.append(data_obj)

    # read data and preprocess
    for data_obj in data_objs:
        data_obj.read(date)

        data_obj._interpolate_if_1d(interp_res) # inline


