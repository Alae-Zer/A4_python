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
    """Gets a sorted list of cities that are acceptable for the specified timeframe.

    A city is acceptable if it is acceptable for every year in the timeframe.
    A city is acceptable for a year if there are no gaps of more than ten days between valid data points.
    """
    res = dict()
    
    #Track counts
    totalCities = 0
    acceptedCities = 0

    #FILE STRUCTURE -- Region,City,State,Lat,Lon,FileName,StartDate,EndDate
    try:
        if(readIntoList(DIRECTORY)):
            inputFileContest = readIntoList(DIRECTORY)
            for line in inputFileContest:
                
                tokens = line.split(",")
                
                #WE UNDERSTAND THAT IT IS SILLY, BUT REMOVES THE FIRST ROW IF HEADERS ARE AVAILABLE, ELSE TRYING TO COLLECT
                if(tokens[0] == "Region" and tokens[1] == "City"):
                    continue
                
                region = tokens[0]
                city = tokens[1]
                state = tokens[2]
                fileName = tokens[5]
                totalCities += 1
                
                try:
                    #FILE STRUCTURE -- "","Date","tmax","tmin","prcp"
                    cityFileReadings = DATA_PATH + "/" + fileName
                    inputCityContest = readIntoList(cityFileReadings)
                    
                    #Store valid dates for each year
                    validDatesByYear = {}
                    
                    #Populate Years based On Range Value
                    for year in range(startYear, (endYear + 1)):
                        validDatesByYear[year] = []
                    
                    for lineCity in inputCityContest:
                        cityTokens = lineCity.split(",")

                        #Skip Line If not enough args, NOT REQUIRED BUT JUST IN CASE
                        if len(cityTokens) != 5:
                            continue

                        date = cityTokens[1]
                        maxTemperature = cityTokens[2]
                        minTemperature = cityTokens[3]

                        #Skip Header or incorrect date line
                        if((date == '"Date"' and maxTemperature == '"tmax"') or (maxTemperature == "NA" or minTemperature == "NA")):
                            continue
                            
                        dateTokens = date.split("-")
                        year = int(dateTokens[0])
                        month = int(dateTokens[1])
                        day = int(dateTokens[2])
                        
                        # Only add if year is in our range
                        if year >= startYear and year <= endYear:
                            validDatesByYear[year].append(datetime.date(year, month, day))
                    
                    #Flag to
                    cityAcceptable = True
                    
                    # Check for gaps in each year
                    # Check for gaps in each year
                    for year in range(startYear, endYear + 1):
                        if len(validDatesByYear[year]) == 0:
                            cityAcceptable = False
                            break
                        
                        # Check forward gaps
                        dates = sorted(validDatesByYear[year])
                        for i in range(1, len(dates)):
                            gap = (dates[i] - dates[i-1]).days
                            if gap >= 10:
                                cityAcceptable = False
                                break
                        
                        # Check backward gaps (descending order)
                        dates_backward = sorted(validDatesByYear[year], reverse=True)
                        for i in range(1, len(dates_backward)):
                            gap = (dates_backward[i-1] - dates_backward[i]).days
                            if gap >= 10:
                                cityAcceptable = False
                                break
                        
                        if not cityAcceptable:
                            break
                    
                    if cityAcceptable:
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
    
    #Sort cities in each region
    for region in res:
        res[region].sort()
    
    #Print results
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
