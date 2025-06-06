import numpy as np
import pandas as pd

from .netcdf import NetCDFReader
from .zarr import ZarrReader

class DataModule:
    def __init__(
        self,
        paths: str or list[str],
        field: str or list[str] = None,
        interp_res: float = None,
        date: str = None,
        lead_time: int or list[int] = None,
        member: int or list[int] = None,
        labels: str or list[str] = None,
        freq: str = '6h',
        **kwargs,
    ) -> None:
        self.labels = labels
        paths = np.atleast_1d(paths)

        data_objs = self._initialize(paths, date, lead_time, freq, field, **kwargs)
        self._read_data(data_objs, interp_res)

    @staticmethod
    def _get_all_dates(date, dates, lead_times, lead_times_nc, freq):
        """Get reference date to be taken from
        zarr files."""

        if date is None:
            if len(dates) == 0:
                raise ValueError("No date is specified for Zarr datasets. Please specify date!")
            elif len(dates) == 1:
                start = dates[0]
                max_lead_time = max(lead_times_nc[0])
            else:
                raise ValueError("Multiple dates specified for Zarr datasets. Please specify date!")
        else:
            assert lead_time is not None, \
                "Lead times have to be specified if date is specified"
            start = date
            max_lead_time = max(lead_times)
        all_dates = pd.date_range(start, periods=max_lead_time, freq=freq)
        end = all_dates[-1]
        #end = start + pd.Timedelta(hours=int(freq[:-1]) * max_lead_time)
        return start, end

    def _initialize(self, paths, date, lead_times, freq, fields, **kwargs):
        """Initialize reader objects
        initialize NetCDF files before Zarr files, as we need information
        about the reference date and lead times to be fetched from Zarr
        """
        data_objs = len(paths) * [None]

        # initialize NetCDF files and do extension checks
        dates = []
        lead_times_nc = []
        zarr_idx = []
        for i, path in enumerate(paths):
            suffix = path.split('.')[-1]
            if suffix == 'nc':
                data_obj = NetCDFReader(path)
                dates.append(data_obj.date)
                lead_times_nc.append(data_obj.lead_times)
                data_objs[i] = data_obj
            elif suffix == 'zarr':
                zarr_idx.append(i)
                data_obj = ZarrReader(path)
            else:
                raise NotImplementedError("Only NetCDF and Zarr formats are currently supported")

        # now initialize Zarr data objects, based on reference date and lead times
        start, end = self._get_all_dates(date, dates, lead_times, lead_times_nc, freq)
        kwargs['paths'] = path
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['frequency'] = freq
        kwargs['select'] = fields
        for i in zarr_idx:
            data_objs[i] = ZarrReader(kwargs)
        return data_objs

    def _read_data(self, data_objs, interp_res):
        # read data and preprocess
        for data_obj in data_objs:
            data_obj._interpolate_if_1d(interp_res) # inline


