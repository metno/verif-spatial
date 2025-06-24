import numpy as np
import xarray as xr
import pandas as pd
from anemoi.datasets import open_dataset

from .convert import convert, convert_inverse
from .datareader import DataReader


class ZarrReader(DataReader):
    """Open Zarr compatible with anemoi.datasets
    Pass any anemoi dataset argument
    """
    def __init__(self, path, field, **kwargs) -> None:
        super().__init__(path, field)

        # Convert from CF compliant to ERA5 standard names
        field_era = []
        for field_ in field:
            field_era.append(convert_inverse[field_])

        ds = open_dataset(path, select=field_era, **kwargs)
        add_member_dim = False
        try:
            field_shape = ds.field_shape
            dims = ['time', 'member', 'x', 'y']
            shape = ds.shape
            if len(shape) == 3:
                # regular xy-grid, no ensemble members
                add_member_dim = True
                members = 1
            elif len(shape) == 4:
                members = shape[2]
            lon=(['x', 'y'], ds.longitude)
            lat=(['x', 'y'], ds.latitude)
        except:
            dims = ['time', 'member', 'latlon']
            shape = ds.shape
            if len(shape) == 2:
                # regular xy-grid, no ensemble members
                add_member_dim = True
                members = 1
            elif len(shape) == 3:
                members = shape[2]
            lon=(['latlon'], ds.longitudes)
            lat=(['latlon'], ds.latitudes)
        
        time = (['time'], pd.date_range(start=kwargs['start'], end=kwargs['end'], freq=kwargs['frequency']))
        member = (['member'], range(members))

        coords = dict(
            longitude=lon,
            latitude=lat,
            member=member,
            time=time,
            reference_time=kwargs['start'],
        )

        ds_ = xr.Dataset()
        all_data = []
        for i in range(len(time[1])):
            all_data.append(ds[i])
        all_data = np.asarray(all_data)

        for key in ds.variables:
            label = convert[key]
            idx = ds.variables.index(key)
            attrs = dict(
                description=label,
                units="",
            )
            da = xr.DataArray(data=all_data[:,idx], dims=dims, coords=coords, attrs=attrs)
            ds_[label] = da

        self.ds = ds_
