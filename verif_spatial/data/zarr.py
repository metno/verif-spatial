import numpy as np
import xarray as xr
from anemoi.datasets import open_dataset

from .convert import convert
from .datareader import DataReader


class ZarrReader(DataReader):
    """Open Zarr compatible with anemoi.datasets
    Pass any anemoi dataset argument
    """
    def __init__(self, **kwargs) -> None:

        ds = open_dataset(**kwargs)
        add_member_dim = False
        try:
            field_shape = ds.field_shape
            dims = ['member', 'time', 'x', 'y']
            shape = ds.shape
            if len(shape) == 3:
                # regular xy-grid, no ensemble members
                add_member_dim = True
            elif len(shape) == 4:
                pass
            lon=(['x', 'y'], ds.longitude)
            lat=(['x', 'y'], ds.latitude)
        except:
            dims = ['member', 'time', 'latlon']
            shape = ds.shape
            if len(shape) == 2:
                # regular xy-grid, no ensemble members
                add_member_dim = True
            elif len(shape) == 3:
                pass
            lon=(['latlon'], ds.longitude)
            lat=(['latlon'], ds.latitude)
        
        coords = dict(
            lon=lon,
            lat=lat,
            time=time,
            reference_time=kwargs['start'],
        )

        ds = xr.Dataset()
        for key in ds.variables:
            label = convert[key]
            idx = ds.variables.index(key)
            attrs = dict(
                description=label,
                units="",
            )
            da = xr.DataArray(data=ds[idx], dims=dims, coords=coords, attrs=attrs)
            ds[label] = da

        self.ds = ds
