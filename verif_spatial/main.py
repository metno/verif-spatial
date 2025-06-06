from data.datamodule import DataModule
from analyse.analyse import Analyse

netcdf = "..."
zarr = "..."

dm = DataModule(paths=["../netcdf/example.nc"])
