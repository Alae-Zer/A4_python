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

def process_temperature_file(filename):
    try:
        lines = readIntoList(filename)
        if (len(lines) == 0):
            return []
    except:
        raise FileNotFoundError(f"Could not open file: {filename}")
        
    outputData = []
    
    for line in lines:
        tokens = line.split(",")
        date = tokens[1]
        tmax = tokens[2]
        tmin = tokens[3]
        if(date == '"Date"' and tmax == '"tmax"'):
            continue
                
        outputData.append({"Date": date, "tmax": tmax, "tmin": tmin})
    
    validTmaxPositions = []
    for i in range(len(outputData)):
        if outputData[i]["tmax"] != "NA":
            validTmaxPositions.append(i)
    
    for i in range(len(outputData)):
        if outputData[i]["tmax"] == "NA":
            prevPos = -1
            nextPos = -1
            
            for pos in validTmaxPositions:
                if pos < i:
                    prevPos = pos
                elif pos > i:
                    nextPos = pos
                    break

            if prevPos != -1 and nextPos != -1:
                prevVal = float(outputData[prevPos]["tmax"])
                nextVal = float(outputData[nextPos]["tmax"])
                outputData[i]["tmax"] = str((prevVal + nextVal) / 2)
            elif prevPos != -1:
                outputData[i]["tmax"] = outputData[prevPos]["tmax"]
            elif nextPos != -1:
                outputData[i]["tmax"] = outputData[nextPos]["tmax"]
    

    validTminPositions = []
    for i in range(len(outputData)):
        if outputData[i]["tmin"] != "NA":
            validTminPositions.append(i)
    
    for i in range(len(outputData)):
        if outputData[i]["tmin"] == "NA":
            prevPos = -1
            nextPos = -1
            
            for pos in validTminPositions:
                if pos < i:
                    prevPos = pos
                elif pos > i:
                    nextPos = pos
                    break
            
            if prevPos != -1 and nextPos != -1:
                prevVal = float(outputData[prevPos]["tmin"])
                nextVal = float(outputData[nextPos]["tmin"])
                value = (prevVal + nextVal) / 2
                outputData[i]["tmin"] = f"{value:.1f}"
            elif prevPos != -1:
                value = float(outputData[prevPos]["tmin"])
                outputData[i]["tmin"] = f"{value:.1f}"
            elif nextPos != -1:
                value = float(outputData[nextPos]["tmin"])
                outputData[i]["tmin"] = f"{value:.1f}"
    
    resultData = []
    for i in range(len(outputData)):
        resultData.append(f"{outputData[i]['Date']},{outputData[i]['tmax']},{outputData[i]['tmin']}")
    
    return resultData

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
    try:
        inputCities = readIntoList(DIRECTORY)
        cityFiles = {}
        
        for cityLine in inputCities:
            tokens = cityLine.split(",")
            if tokens[0] == "Region":
                continue
                
            fileName = tokens[5]
            cityName = tokens[1]
            state = tokens[2]
            
            cityFullName = f"{cityName} {state}"
            if cityFullName in cities:
                filePath = DATA_PATH + "/" + fileName
                cityFiles[cityFullName] = filePath
        
        cityData = {}
        for city, filePath in cityFiles.items():
            processedData = process_temperature_file(filePath)
            
            dateDict = {}
            for line in processedData:
                tokens = line.split(',')
                if len(tokens) >= 3 and tokens[0]:
                    date = tokens[0].strip('"')
                    tmax = tokens[1]
                    tmin = tokens[2]
                    dateDict[date] = {"tmax": float(tmax), "tmin": float(tmin)}
            
            cityData[city] = dateDict
        
        allDates = []
        for year in range(startYear, endYear + 1):
            for month in range(1, 13):
                daysInMonth = 31
                if month in [4, 6, 9, 11]:
                    daysInMonth = 30
                elif month == 2:
                    if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
                        daysInMonth = 29
                    else:
                        daysInMonth = 28
                
                for day in range(1, daysInMonth + 1):
                    dateStr = f"{year}-{month:02d}-{day:02d}"
                    allDates.append(dateStr)
        
        outputLines = ["Date,Temperature"]
        
        for date in allDates:
            tmaxSum = 0
            tminSum = 0
            validCities = 0
            
            for city, data in cityData.items():
                if date in data:
                    tmaxSum += data[date]["tmax"]
                    tminSum += data[date]["tmin"]
                    validCities += 1
            
            if validCities > 0:
                avgHigh = tmaxSum / validCities
                avgLow = tminSum / validCities
                
                dailyAvgF = (avgHigh + avgLow) / 2
                
                dailyAvgC = (dailyAvgF - 32) * 5/9
                
                outputLines.append(f"{date},{dailyAvgC:.1f}")
        
        writeListToFile(outputLines, outputFileName)
        
        return True
        
    except Exception as e:
        print(f"Error in create_regional_file: {e}")
        raise


def consolidate_regions(fileName):
    try:
        consolidatedLines = ["Region,Date,Temperature"]
        fileName = f"./data/outputs/{fileName}.csv"
        
        for region in range(1, 10):
            regionFile = f"./data/outputs/{region}region.csv"
            
            try:
                regionData = readIntoList(regionFile)
                
                for i in range(1, len(regionData)):
                    line = regionData[i]
                    

                    if line == consolidatedLines[0]:
                        continue

                    parts = line.split(',')
                    if len(parts) == 2:
                        date = parts[0]
                        temp = parts[1]
                        consolidatedLines.append(f"{region},{date},{temp}")
            
            except FileNotFoundError:
                print(f"Warning: Could not find region file {regionFile}")
                continue
        
        writeListToFile(consolidatedLines, fileName)
        print(f"Regions consolidated to {fileName}")
        return True
        
    except Exception as e:
        print(f"Error consolidating regions: {e}")
        return False


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
    elif len(sys.argv) == 2:
        fileName = sys.argv[1]
        consolidate_regions(fileName)
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
