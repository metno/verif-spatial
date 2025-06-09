import numpy as np
import pandas as pd

from .netcdf import NetCDFReader
from .zarr import ZarrReader
from .utils import time_to_unix


class DataModule:
    """DataModule class that takes care of all the data

    Args:
        path: str or list[str]
            Path to NetCDF or Zarr file(s) 
        field: str or list[str] = None
            Field(s) to load, cf-compliant
        lead_time: int or list[int] = None,
            Lead time(s) to include, given in multiples of freq
        member: int or list[int] = None
            Member(s) to load
        label: str or list[str] = None
            Label the path(s). If given, the length has to match
            the length of path
        interp_res: float = None
            Interpolation resolution in degrees
        reference_time: str = None
            Reference time of frame, required if Zarr format
        freq: str = '6h'
            Frequency of lead times
        kwargs: dict
            Keyword arguments that go into anemoi.datasets.open_dataset
    """
    def __init__(
        self,
        path: str or list[str],
        field: str or list[str] = None,
        lead_time: int or list[int] = None,
        member: int or list[int] = None,
        label: str or list[str] = None,
        interp_res: float = None,
        reference_time: str = None,
        freq: str = '6h',
        **kwargs,
    ) -> None:

        self._atleast_1d(path, field, lead_time, member, label)
        self.data_obj = len(self.path) * [None]
        reference_time_nc, lead_times_nc, zarr_idx = self._initialize_netcdf()
        if len(zarr_idx) > 0:
            start, end = self._get_start_end(reference_time_nc, lead_times_nc, reference_time, lead_time, freq)
            self._initialize_zarr(start, end, freq, zarr_idx, **kwargs)
        self._preprocess_data(interp_res)


    def _atleast_1d(self, path, field, lead_time, member, label):
        """Ensure that path, field, lead_time, member and label are
        arrays to make rest of the code generic even with only one
        element. Keep None if None
        """
        self.path = np.atleast_1d(path)
        self.field = None if field is None else np.atleast_1d(field)
        self.lead_time = None if lead_time is None else np.atleast_1d(lead_time)
        self.member = None if member is None else np.atleast_1d(member)
        if label is not None:
            self.label = np.atleast_1d(label)
            assert len(self.label) == len(self.path), \
                    "Number of labels have to match number of paths!"
        else:
            self.label = None

    
    def _initialize_netcdf(self):
        """
        """

        reference_time_nc = []
        lead_times_nc = []
        zarr_idx = []
        for i, _path in enumerate(self.path):
            suffix = _path.split('.')[-1]
            if suffix == 'nc':
                _data_obj = NetCDFReader(_path)
                reference_time_nc.append(_data_obj.reference_time)
                lead_times_nc.append(_data_obj.lead_times)
                self.data_obj[i] = _data_obj
            elif suffix == 'zarr':
                zarr_idx.append(i)
            else:
                raise NotImplementedError("Only NetCDF and Zarr formats are currently supported")
        return reference_time_nc, lead_times_nc, zarr_idx


    def _get_start_end(self, reference_time_nc, lead_times_nc, reference_time, lead_time, freq):
        """Get start and end time to be used in Zarr.
        For flexibility reasons, we work in unix time in this class.

        To fetch data from Zarr archives, we need start and end times.
        These are either taken from input arguments (prioritized) or
        from the minimum and maximum values found in NetCDF files.
        """
        
        # get reference time as a datetime object
        if reference_time is not None:
            start = time_to_datetime(reference_time)
        elif len(reference_time_nc) > 0:
            start = min(reference_time_nc)
        elif len(lead_times_nc) > 0:
            start = np.inf
            for lead_times_nc_ in lead_times_nc:
                start = min(start, min(lead_times_nc_))
        else:
            raise ValueError("Reference time is not obtained, please specify reference_time")

        # extract frequency unit and quantity
        freq_unit = freq[-1]
        freq_quantity = int(freq[:-1])

        # get end time as a datetime object
        if lead_time is not None:
            assert reference_time is not None, "'lead_time' has to be accommodated by 'reference_time'"
            end = start + pd.Timedelta(max(lead_time) * freq_quantity, freq_unit)
        elif len(lead_times_nc) > 0:
            end = -np.inf
            for lead_times_nc_ in lead_times_nc:
                end = max(end, max(lead_times_nc_))
        else:
            raise ValueError("Lead time is not obtained, please specify lead_time")
        return start, end


    def _initialize_zarr(self, start, end, freq, zarr_idx, **kwargs):
        """Now initialize Zarr data objects, based on reference date and lead times."""
        kwargs['path'] = self.path
        kwargs['start'] = start
        kwargs['end'] = end
        kwargs['frequency'] = freq
        kwargs['select'] = self.field
        for i in zarr_idx:
            self.data_obj[i] = ZarrReader(kwargs)


    def _preprocess_data(self, interp_res):
        """Preprocess data."""
        for data_obj_ in self.data_obj:
            data_obj_._interpolate_if_1d(interp_res) # inline


# Unused code from here


    def _convert_to_unix(self, reference_time, lead_time, freq):
        """For flexibility reasons, we work in unix time
        in this class.
        """
        if isinstance(reference_time, str):
            reference_time = pd.Timestamp(reference_time)
        # extract frequency unit and quantity
        self.freq_unit = freq[-1]
        self.freq_quantity = int(freq[:-1])
        if lead_time is None:
            self.lead_time_unix = None
        else:
            self.lead_time_unix = []
            for _lead_time in lead_time:
                delta = pd.Timedelta(_lead_time * self.freq_quantity, self.freq_unit)
                lead_time_timestamp = reference_time + delta
                self.lead_time_unix.append(lead_time_timestamp.strftime('%s'))
        self.lead_time = lead_time
        self.reference_time = reference_time
        self.reference_time_unix = None if reference_time is None else reference_time.strftime('%s')


    @staticmethod
    def _get_all_dates(date, dates, lead_times, lead_times_nc, freq):
        """Get reference date to be taken from
        zarr files."""

        if date is None:
            if len(dates) == 0:
                raise ValueError("No date is specified for Zarr datasets. Please specify date!")
            elif len(dates) == 1:
                start = dates[0]
                print(lead_times_nc)
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





    def _initialize(self, **kwargs):
        """Initialize reader objects
        initialize NetCDF files before Zarr files, as we need information
        about the reference date and lead times to be fetched from Zarr
        """
        data_obj = len(self.path) * [None]

        # initialize NetCDF files and perform extension checks
        dates = []
        lead_times_nc = []
        zarr_idx = []
        for i, _path in enumerate(self.path):
            suffix = _path.split('.')[-1]
            if suffix == 'nc':
                _data_obj = NetCDFReader(_path)
                dates.append(_data_obj.reference_time)
                lead_times_nc.append(data_obj.lead_time)
                data_obj[i] = _data_obj
            elif suffix == 'zarr':
                zarr_idx.append(i)
                _data_obj = ZarrReader(path)
            else:
                raise NotImplementedError("Only NetCDF and Zarr formats are currently supported")

        self._convert_to_unix(reference_time, self.lead_time, freq)    
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

