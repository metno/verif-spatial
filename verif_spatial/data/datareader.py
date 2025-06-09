import numpy as np
import scipy.interpolate


class DataReader:
    """Data reader base class"""
    def __init__(
        self,
        path,
    ) -> None:
        self.path = path

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
        for field in ds.keys():
            field_2d = ds[field]
            interpolator = scipy.interpolate.NearestNDInterpolator(in_coords, field_2d)
            q = interpolator(out_coords)
            ens_size, lead_time, latlon = ds[field].shape
            ds[field] = xr.DataArray(q.reshape(lat_grid.shape), dims=('members', 'leadtimes', 'x', 'y'))

    def _interpolate_if_1d(
        self,
        interp_res: float,
    ) -> None:
        """Interpolate all dataset fields if they only have exactly one spatial dimension."""
        if len(self.ds.location) == 1:
            self._interpolate_all_fields(interp_res)

    def get_ds(self):
        return self.ds
