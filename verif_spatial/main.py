from data.datamodule import DataModule
from analyse.analyse import Analyse
from visualise.plot2d import Plot2d

dm = DataModule("../netcdf/n320_pred_20230601T06Z.nc", field=["air_temperature_2m", "air_pressure_at_sea_level"])

pt = Plot2d(dm.data_obj)
pt.add_colormesh('air_temperature_2m', units='K', cmap='turbo')
#pt.add_contour_lines('air_pressure_at_sea_level')
pt(path_out='this.png')
