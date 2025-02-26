import datetime
import TemperatureHelper
from FileUtils import readIntoList, writeListToFile
#import matplotlib.pyplot as plt
import sys


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
   res = dict()
   totalCities = 0
   acceptedCities = 0
   
   try:
       if(readIntoList(DIRECTORY)):
           inputFileContest = readIntoList(DIRECTORY)
           for line in inputFileContest:
               tokens = line.split(",")
               
               if(tokens[0] == "Region" and tokens[1] == "City"):
                   continue
               
               region = tokens[0]
               city = tokens[1]
               state = tokens[2]
               fileName = tokens[5]
               startDate = tokens[6]
               
               # Skip cities that start after our range
               startYear_city = int(startDate.split("-")[0])
               if startYear_city > startYear:
                   continue
                   
               totalCities += 1
               
               try:
                   cityFileReadings = DATA_PATH + "/" + fileName
                   inputCityContest = readIntoList(cityFileReadings)
                   
                   consecutiveNACount = 0
                   cityIsGood = False
                   validReadingsInRange = 0
                   MINIMUM_VALID_READINGS = 1
                   
                   for lineCity in inputCityContest:
                       cityTokens = lineCity.split(",")
                       
                       date = cityTokens[1]
                       maxTemperature = cityTokens[2]
                       minTemperature = cityTokens[3]
                       
                       if(date == '"Date"' and maxTemperature == '"tmax"' and minTemperature == '"tmin"'):
                           continue
                       
                       dateTokens = date.split("-")
                       year = int(dateTokens[0])
                       month = int(dateTokens[1])
                       day = int(dateTokens[2])
                       
                       if (year >= startYear and year <= endYear):
                           if (maxTemperature == "NA" or minTemperature == "NA"):
                               consecutiveNACount += 1
                               if consecutiveNACount >= 10:
                                   break
                           else:
                               consecutiveNACount = 0
                               validReadingsInRange += 1
                               if validReadingsInRange >= MINIMUM_VALID_READINGS:
                                   cityIsGood = True
                   
                   if cityIsGood and consecutiveNACount < 10:
                       regionNum = int(region)
                       if regionNum not in res:
                           res[regionNum] = []
                       res[regionNum].append(f"{city} {state}")
                       acceptedCities += 1
               
               except:
                   print(f"Unable to read {cityFileReadings}")
                   continue
       else:
           raise FileNotFoundError()
   except:
       print("Error reading city information file")
   
   for region in res:
       res[region].sort()
   
   totalAccepted = 0
   for region in sorted(res.keys()):
       citiesInRegion = len(res[region])
       totalAccepted += citiesInRegion
       print(f"Region {region} ({citiesInRegion} cities):\n")
       for city in res[region]:
           print(f"\t{city}")
       print()
   
   print(f"Found {totalAccepted} acceptable cities for years {startYear} to {endYear}.")
   
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
    #plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def annual_means_combined(regions, years, patterns, consolidatedFile):
    """Creates and saves a single graph showing the annual means
    for all the regions, one series per region.
    Use the specified patterns for the legend.
    """
    #plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def single_day_per_region(regions, years, month, day, consolidatedFile):
    """Creates and saves one graph per region, each showing the
    temperature on the specified day for each specified year.
    """
    #plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here


def single_day_combined(regions, years, month, day, patterns, consolidatedFile):
    """Creates and saves a single graph showing the temperatures on
    the specified day for the specified years, one series per region.
    Use the specified patterns for the legend.
    """
    #plt.rcParams["figure.figsize"] = [10, 6]  # bigger than default
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)

    # your code here

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        try:
            startYear = int(sys.argv[1])
            endYear = int(sys.argv[2])
            get_acceptable_cities(startYear, endYear)
        except ValueError:
            print("Error: Start year and end year must be integers")
    else:
        print("Usage: python a4functions.py <start_year> <end_year>")
        print("Example: python a4functions.py 1994 2023")
