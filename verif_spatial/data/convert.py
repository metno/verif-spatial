# Convert ERA5 names to CF compliant names
# and units. Zarr files are expected to be in 
# ERA5 names (2t, 10u, 10v, tp etc..) and 
# NetCDF files are expected to already contain
# CF compliant names and units

convert = {
    "2t": "air_temperature_2m",
    "2d": "dew_point_temperature_2m",
    "10u": "x_wind_10m",
    "10v": "y_wind_10m",
    "msl": "air_pressure_at_sea_level",
}
convert_inverse = {
    "air_temperature_2m": "2t",
    "dew_point_temperature_2m": "2d",
    "x_wind_10m": "10u",
    "y_wind_10m": "10v",
    "air_pressure_at_sea_level": "msl",
}
