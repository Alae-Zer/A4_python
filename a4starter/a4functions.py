import datetime
import TemperatureHelper
import matplotlib.pyplot as plt


DATA_PATH = "data/original"
DIRECTORY = DATA_PATH + "/" + "city_info.csv"
MONTH_NAMES = [
    "January",
    "February",
    "March",
    "April",
    "May",
    "June",
    "July",
    "August",
    "September",
    "October",
    "November",
    "December",
]


def get_acceptable_cities(startYear, endYear):
    """Gets a sorted list of cities that are acceptable for the specified timeframe.

    A city is acceptable if it is acceptable for every year in the timeframe.
    A city is acceptable for a year if there are no gaps of more than ten days between valid data points.
    """
    res = dict()

    # your code here

    return res


def create_regional_file(cities, startYear, endYear, outputFileName):
    """For each date in the range, calculate a single temperature as follows:
    1. Find the average high of the three input cities.
    2. Find the average low of the three input cities.
    (Missing data points for min and max are filled in from surrounding dates.)
    3. Average the average high and the average low to get a single daily temperature.
    4. Convert the daily temperature to Celsius.
    5. Create a file containing the daily temperatures for for each day in the range.
       Store the Celsius temperatures to one decimal place of precision.
    """
    pass
    # your code here


def consolidate_regions(file_name):
    """Consolidates the nine regional files into a single file."""
    pass

    # your code here


def annual_means_per_region(regions, years, consolidatedFile):
    """Creates and saves one graph per region, each showing the
    annual mean temperatures for that region.
    """
    plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def annual_means_combined(regions, years, patterns, consolidatedFile):
    """Creates and saves a single graph showing the annual means
    for all the regions, one series per region.
    Use the specified patterns for the legend.
    """
    plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def single_day_per_region(regions, years, month, day, consolidatedFile):
    """Creates and saves one graph per region, each showing the
    temperature on the specified day for each specified year.
    """
    plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def single_day_combined(regions, years, month, day, patterns, consolidatedFile):
    """Creates and saves a single graph showing the temperatures on
    the specified day for the specified years, one series per region.
    Use the specified patterns for the legend.
    """
    plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here
