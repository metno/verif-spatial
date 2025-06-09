import numpy as np
import xarray as xr
import scipy.interpolate


class DataReader:
    """Data reader base class"""
    def __init__(
        self,
        path,
        field,
    ) -> None:
        self.label = path
        self.field = field

    @staticmethod
    def _create_mesh(
        lat: np.ndarray,
        lon: np.ndarray, 
        interp_res: float,
    ) -> (np.ndarray, np.ndarray):
        """Create latlon-regular mesh
        """
        lat = np.arange(lat.min(), lat.max(), interp_res)
        lon = np.arange(lon.min(), lon.max(), interp_res)
        lat_grid, lon_grid = np.meshgrid(lat, lon)
        return lat_grid.T, lon_grid.T

    def _interpolate_all_fields(
        self,
        field: list[str],
        interp_res: float,
    ) -> None:
        """Interpolate all the dataset fields"""

        # input grid
        lat = self.ds.latitude
        lon = self.ds.longitude
        in_coords = np.asarray([lon, lat], dtype=np.float32).T

        # output grid
        lat_grid, lon_grid = self._create_mesh(lat, lon, interp_res)
        out_coords = np.asarray([lon_grid.flatten(), lat_grid.flatten()], dtype=np.float32).T

        # interpolate from input grid to output grid
        for field_ in field:
            field_2d = self.ds[field_]
            try:
                lead_times, members, latlon = field_2d.shape
            except:
                continue
            if members > 1:
                continue
            field_2d_ = np.empty((lead_times, members, *lat_grid.shape))
            for lead_time in range(lead_times):
                for member in range(members):
                    interpolator = scipy.interpolate.NearestNDInterpolator(in_coords, field_2d[lead_time, member])
                    q = interpolator(out_coords)
                    field_2d_[lead_time, member] = q.reshape(lat_grid.shape)
            self.ds['x'] = np.arange(lat.min(), lat.max(), interp_res)
            self.ds['y'] = np.arange(lon.min(), lon.max(), interp_res)
            self.ds[field_] = xr.DataArray(field_2d_, dims=('leadtimes', 'members', 'x', 'y'))

    def _interpolate_if_1d(
        self,
        field: list[str],
        interp_res: float,
    ) -> None:
        """Interpolate all dataset fields if they only have exactly one spatial dimension."""
        if len(self.ds.location.shape) == 1:
            self._interpolate_all_fields(field, interp_res)
