import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import cartopy.feature as cfeature

from .visualise import Visualise


class Plot2d(Visualise):
    """Plot 2d field.

    kwargs go into matplotlib imshow
    """

    def add_colormesh(
            self, 
            field: str, 
            lead_time: int or list[int] = 0, 
            member: int or list[int] = 0,
            units: str = '',
            title: str = '',
            path_out: str = None,
            show: bool = True,
            **kwargs,
        ) -> None:
        ax = self.axs[0,0]
        for data_obj_ in self.data_obj:
            ds = data_obj_.ds
            ax.add_feature(cfeature.COASTLINE, edgecolor='black')
            ax.add_feature(cfeature.BORDERS, linestyle=':', edgecolor='black')
            ax.add_feature(cfeature.LAND, edgecolor='black')
            ax.add_feature(cfeature.OCEAN, edgecolor='black')
            im = ax.pcolormesh(ds.y, ds.x, ds[field][member, lead_time], **kwargs)
        cbax = self.fig.colorbar(im, ax=self.axs.ravel().tolist())
        cbax.set_label(f"{field} ({units})")
        return im


    def add_contour_lines(
            self,
            field: str,
            **kwargs,
            #linewidths: float = 1.0,
            #colors: str = 'magenta',
        ) -> None:
        ax = self.axs[0,0]
        for data_obj_ in self.data_obj:
            ds = data_obj_.ds
            im = ax.contour(ds.y, ds.x, field, **kwargs)
            ax.clabel(im, inline=True, fontsize=8, fmt='%1.0f')
        return im
