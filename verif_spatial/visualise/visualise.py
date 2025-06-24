import matplotlib.pyplot as plt
import cartopy.crs as ccrs


class Visualise:
    """Visualise base class."""

    def __init__(self, data_obj) -> None:
        self.data_obj = data_obj
        projection = ccrs.PlateCarree()
        self.fig, self.axs = plt.subplots(1,1, figsize=(6,4), squeeze=False, subplot_kw={'projection': projection})

        print(f"Plotting '{self}'")


    def __call__(self, path_out: str = None, show: bool = True, title: str = ''):
        """ """
        self.fig.suptitle(title)
        #self.fig.tight_layout()
        if path_out is not None:
            self.fig.savefig(path_out)
            print(f"Saving figure to '{path_out}'")
        if show:
            self.fig.show()
        return self.fig


