from data.datamodule import DataModule
from analyse.analyse import Analyse
from visualise.plot2d import Plot2d

dm = DataModule(path=["../netcdf/n320_pred_20230601T06Z.nc"])

pt = Plot2d('air_temperature_2m')
pt(dm.data_obj)

for data_obj_ in dm.data_obj:
    print(data_obj_.ds)


