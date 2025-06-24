import numpy as np
import xarray as xr
import scipy.interpolate
from scipy.spatial import cKDTree

class DataReader:
    """Data reader base class"""
    def __init__(
        self,
        path,
        field,
    ) -> None:
        self.label = path
        self.field = field
        add_member_dim = False

        print(f"Reading '{path}'")

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

    def _add_member_dim(self, shape, lat, lon, regular=False):
        """Add a member dimension to the shape if it is not present."""
        if regular:
            dims = ['time', 'member', 'x', 'y']
            if len(shape) == 3:
                # regular xy-grid, no ensemble members
                self.add_member_dim = True
                members = 1
            elif len(shape) == 4:
                members = shape[2]
            lat_=(['x', 'y'], np.array(lat))
            lon_=(['x', 'y'], np.array(lon))
        else:
            dims = ['time', 'member', 'latlon']
            if len(shape) == 2:
                # regular xy-grid, no ensemble members
                self.add_member_dim = True
                members = 1
            elif len(shape) == 3:
                members = shape[2]
            lat_=(['latlon'], np.array(lat))
            lon_=(['latlon'], np.array(lon))
        member = (['member'], range(members))
        return lon_, lat_, member, dims

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
        tree = cKDTree(in_coords)

        # output grid
        lat_grid, lon_grid = self._create_mesh(lat, lon, interp_res)
        out_coords = np.asarray([lon_grid.flatten(), lat_grid.flatten()], dtype=np.float32).T
        _, indices = tree.query(out_coords, k=1)
        self.ds['x'] = np.arange(lat.min(), lat.max(), interp_res)
        self.ds['y'] = np.arange(lon.min(), lon.max(), interp_res)
        self.ds['latitude'] = (['x', 'y'], lat_grid)
        self.ds['longitude'] = (['x', 'y'], lon_grid)

        # interpolate from input grid to output grid
        for field_ in field:
            field_2d = self.ds[field_]
            try:
                lead_times, members, latlon = field_2d.shape
            except:
                continue
            if members > 1:
                continue
            out_shape = (lead_times, members, lat_grid.shape[0], lat_grid.shape[1])
            q = np.array(field_2d[..., indices]).reshape(out_shape)
            self.ds[field_] = xr.DataArray(q, dims=('leadtimes', 'members', 'x', 'y'))

    def _interpolate_if_1d(
        self,
        field: list[str],
        interp_res: float,
    ) -> None:
        """Interpolate all dataset fields if they only have exactly one spatial dimension."""
        if len(self.ds.latitude.shape) == 1:
            self._interpolate_all_fields(field, interp_res)
