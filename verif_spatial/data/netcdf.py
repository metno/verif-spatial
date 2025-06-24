# Read NetCDF file using xarray. The NetCDF files should be
# compatible with bris-inference, with the following shapes:
#
# Bris inference:
# ...
#
# Anemoi inference:
# dimensions:
#        values = 542080 ;
#        time = 41 ;
#variables:
#        int time(time) ;
#                time:units = "seconds since 2020-01-01 00:00:00" ;
#                time:long_name = "time" ;
#                time:calendar = "gregorian" ;
#        float latitude(values) ;
#                latitude:units = "degrees_north" ;
#                latitude:long_name = "latitude" ;
#        float longitude(values) ;
#                longitude:units = "degrees_east" ;
#                longitude:long_name = "longitude" ;
#        float q_50(time, values) ;
#                q_50:_FillValue = NaNf ;
#                q_50:fill_value = NaN ;
#                q_50:missing_value = NaNf ;
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
        field,
    ) -> None:
        super().__init__(path, field)

        ds = xr.open_dataset(path)
        static_fields = ['time', 'longitude', 'latitude']
        static_fields.extend(field)
        regular = 'x' in ds.keys()
        lon, lat, member, dims = self._add_member_dim(ds[field[0]].shape, ds.latitude, ds.longitude, regular)
        if regular:
            static_fields.append('x')
            static_fields.append('y')

        self.lead_times = time_to_datetime(ds.time)
        self.reference_time = self.lead_times[0]

        coords = dict(
            longitude=lon,
            latitude=lat, 
            member=member,
            time=self.lead_times,
            reference_time=self.reference_time,
        )

        ds_ = xr.Dataset()
        for field_ in field:
            attrs = dict(
                description=field_,
                units="",
            )
            data = np.array(ds[field_])
            if self.add_member_dim:
                data = data[:, None]
            da = xr.DataArray(data=data, dims=dims, coords=coords, attrs=attrs)
            ds_[field_] = da

        self.ds = ds_
        #self.ds = ds[static_fields]
        #self.lead_times = time_to_datetime(self.ds.time)
        #self.reference_time = self.lead_times[0]
        #self._filter_field(field)
        #member = (['member'], range(members))

    def _filter_field(self, field):
        """ """
        pass
