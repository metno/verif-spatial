from data.datamodule import DataModule
from analyse.analyse import Analyse

dm = DataModule(path=["../netcdf/n320_pred_20230601T06Z.nc"])

for data_obj_ in dm.data_obj:
    print(data_obj_.ds)
