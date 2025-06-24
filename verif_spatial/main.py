from data.datamodule import DataModule
from analyse.analyse import Analyse
from visualise.plot2d import Plot2d

paths = [
    #"/lustre/storeB/project/nwp/bris/experiments/legendary_gnome/r4/inference/step_000150/predictions/era5_168hfc_2024-06-01T00.npy",
    #"/lustre/storeB/project/nwp/bris/experiments/legendary_gnome/r4/inference/step_000150/predictions/meps_168hfc_2024-06-01T00.npy",
    "/lustre/storeB/project/nwp/bris/experiments/cloudy_skies/inference/r4/cs_r4_pred_20230101T00Z.nc",
    #"/lustre/storeB/project/nwp/bris/datasets/aifs-meps-2.5km-2020-2024-6h-v6.zarr",
]
    
dm = DataModule(paths, field=["air_temperature_2m", "air_pressure_at_sea_level"])

pt = Plot2d(dm.data_obj)
pt.add_colormesh('air_temperature_2m', member=0, lead_time=0, units='K', cmap='turbo')
#pt.add_contour_lines('air_pressure_at_sea_level')
pt(path_out='this.png')
