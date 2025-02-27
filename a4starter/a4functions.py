import os
import random
import sys
import datetime
from FileUtils import readIntoList, writeListToFile
import TemperatureHelper
#import matplotlib.pyplot as plt



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

    "We assume files are sorted and all dates presented, otherwise we will create a sort function"
    "We were confused by session logs and tried to use datetime objects"
    "But decided to keep this approach as more simple and efficient"
 
    #Count variables and output
    res = dict()
    totalCities = 0
    acceptedCities = 0
   
    #Try to open file
    try:
        inputFileContest = readIntoList(DIRECTORY)
        #Chech if not empty - then call again and extract (Inefficient but works)
        if(len(inputFileContest) !=0):
            #LOOP through lines
            for line in inputFileContest:
                #Split lines to tokens
                tokens = line.split(",")
                
                #Skip header
                if(tokens[0] == "Region" or tokens[1] == "City"):
                    continue

                totalCities += 1
                
                #Assign variables to tokens
                region = tokens[0]
                city = tokens[1]
                state = tokens[2]
                fileName = tokens[5]
                startDate = tokens[6]
                
                #Mark city as Unacceptable if out of our range
                recordingStartedYear = int(startDate.split("-")[0])
                if recordingStartedYear > startYear:
                    continue
                
                #Try to open second file based on previous readings
                try:
                    cityFileReadings = DATA_PATH + "/" + fileName

                    if not readIntoList(cityFileReadings):
                        raise FileNotFoundError()
                    
                    inputCityContest = readIntoList(cityFileReadings)
                    
                    #variables to accept or decline city
                    countNA = 0
                    cityIsGood = False
                    validReadingsInRange = 0
                    
                    #LOOP through city file
                    for lineCity in inputCityContest:
                        #Split line
                        cityTokens = lineCity.split(",")
                        
                        #Extract data required for processing
                        date = cityTokens[1]
                        maxTemperature = cityTokens[2]
                        minTemperature = cityTokens[3]
                        
                        #Skip header
                        if(date == '"Date"' and maxTemperature == '"tmax"' and minTemperature == '"tmin"'):
                            continue
                        
                        #Remove Year
                        dateTokens = date.split("-")
                        year = int(dateTokens[0])
                        
                        #Check if year is correct
                        if (year >= startYear and year <= endYear):
                            #If data is incorrect  - Add counter
                            if (maxTemperature == "NA" or minTemperature == "NA"):
                                countNA += 1
                                #If accumulator achieved max - break loop and keep False for city
                                if countNA >= 10:
                                    break
                            else:
                                #Reset counter
                                countNA = 0
                                validReadingsInRange += 1
                                if validReadingsInRange >= 1:
                                    cityIsGood = True
                    
                    #Store city 
                    if cityIsGood and countNA < 10:
                        regionNum = int(region)
                        #Add region Number to Output
                        if regionNum not in res:
                            #Initialize  an array for the region num
                            res[regionNum] = []
                        res[regionNum].append(f"{city} {state}")
                        acceptedCities += 1
                
                except:
                    print(f"Unable to read {cityFileReadings}")
                    continue
        else:
            raise FileNotFoundError()
    except:
        print(f"Unable to read {DIRECTORY}")
    
    #Sort by region
    for region in res:
        res[region].sort()
    
    #Output
    print()
    print()
    print(f"Processed {totalCities} cities")
    print()
    print()
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

def get_three_random_cities_per_region(startYear, endYear):
    
    outputSelected = {}
    acceptableCities = get_acceptable_cities(startYear, endYear)
    
    #LOOP region
    for region in acceptableCities:
        outputSelected[region] = []
        cities = acceptableCities[region]

        if(len(cities) < 3):
            outputSelected = {}
            return outputSelected
        #print(region)
        
        #LOOP CITY
        while True:
            randomCity = random.choice(cities)
            
            if randomCity in outputSelected[region]:
                continue
            #print(randomCity)
            outputSelected[region].append(randomCity)
            
            if len(outputSelected[region]) == 3:
                break
    
    return outputSelected

def create_regional_file(cities, startYear, endYear, outputFileName):
    """For each date in the range, calculate a single temperature as follows:
    1. Find the average high of the three input cities.
    2. Find the average low of the three input cities.
    (Missing data points for min and max are filled in from surrounding dates.)
    3. Average the average high and the average low to get a single daily temperature.
    4. Convert the daily temperature to Celsius.
    5. Create a file containing the daily temperatures for each day in the range.
       Store the Celsius temperatures to one decimal place of precision.
    """
    
    
    try:
        inputCities = readIntoList(DIRECTORY)

        highAccum = 0
        lowAccum = 0
        for cityLine in inputCities:
            tokens = cityLine.split(",")
            fileName = tokens[5]
            cityName = tokens[1]
            state = tokens[2]

            if fileName == "FileName" and cityName == "City":
                continue
            for city in cities:
                if (cityName +" " + state) == city:
                    filePath = DATA_PATH+ "/" + fileName
            inputTemperatures = readIntoList(filePath)
            for record in inputTemperatures:
                tokensOne = record.split(",")
                tmax = tokensOne[2]
                tmin = tokensOne[3]

                if (tmax == "NA")

    except:
        raise FileNotFoundError


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
            #get_acceptable_cities(startYear, endYear)
            dictionary = get_three_random_cities_per_region(startYear,endYear)
            for x,y in sorted(dictionary.items()):
                outPutfile= "./data/outputs/"+ str(x) +"region.csv"
                cities = y
                create_regional_file(cities,startYear,endYear,outPutfile)
        except ValueError:
            print("Error: Start year and end year must be integers")
    else:
        print("Usage: python a4functions.py <start_year> <end_year>")
        print("Example: python a4functions.py 1994 2023")

        #change back to 3
    # if len(sys.argv) == 2:
    #     try:
    #         var = sys.argv[1].split(" ")
    #         # replace var with sys.argv and add 1 to index
    #         startYear = int(var[0])
    #         endYear = int(var[1])
    #         get_acceptable_cities(startYear, endYear)
    #     except ValueError:
    #         print("Error: Start year and end year must be integers")
    # else:
    #     print("Usage: python a4functions.py <start_year> <end_year>")
    #     print("Example: python a4functions.py 1994 2023")
