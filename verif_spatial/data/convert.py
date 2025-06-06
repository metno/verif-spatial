# Convert ERA5 names to CF compliant names
# and units. Zarr files are expected to be in 
# ERA5 names (2t, 10u, 10v, tp etc..) and 
# NetCDF files are expected to already contain
# CF compliant names and units

convert = {
    "2t": "air_temperature_2m",
    "2d": "dew_point_temperature_2m",
    "10u": "wind_speed_x_10m",
    "10v": "wind_speed_y_10m",
}
