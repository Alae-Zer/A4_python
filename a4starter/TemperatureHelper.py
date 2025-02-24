import numpy as np


class TemperatureHelper(object):
    # Initialize with data from specified file.
    def __init__(self, filename):
        self.rawdata = dict()

        # your code here

    # Get the daily temperatures for the given year and region.
    def get_yearly_temperatures(self, region, year):
        temperatures = []

        # your code here

        return np.array(temperatures)

    # Get the daily temperature for the given region and date (year, month, day).
    def get_daily_temperature(self, region, year, month, day):
        assert region in self.rawdata, "requested region is not available"
        assert (
            year in self.rawdata[region]
        ), f"{year} year is not available for {region}"
        assert month in self.rawdata[region][year], "requested month is not available"
        assert (
            day in self.rawdata[region][year][month]
        ), "requested day is not available"
        return self.rawdata[region][year][month][day]
