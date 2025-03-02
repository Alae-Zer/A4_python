import os
import random
import sys
import datetime
from FileUtils import readIntoList, writeListToFile
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

def process_temperature_file(filename):
    try:
        lines = readIntoList(filename)
        if (len(lines) == 0):
            return []
    except:
        raise FileNotFoundError(f"Could not open file: {filename}")
        
    outputData = []
    
    #Loop through each line in the file and extract data
    for line in lines:
        tokens = line.split(",")
        date = tokens[1]
        tmax = tokens[2]
        tmin = tokens[3]
        if(date == '"Date"' and tmax == '"tmax"'):
            continue
                
        outputData.append({"Date": date, "tmax": tmax, "tmin": tmin})
    
    #Find positions with valid tmax values
    validTmaxPositions = []
    for i in range(len(outputData)):
        if outputData[i]["tmax"] != "NA":
            validTmaxPositions.append(i)
    
    #Fill in missing tmax values
    for i in range(len(outputData)):
        if outputData[i]["tmax"] == "NA":
            prevPos = -1
            nextPos = -1
            
            #Find previous and next valid positions
            for pos in validTmaxPositions:
                if pos < i:
                    prevPos = pos
                elif pos > i:
                    nextPos = pos
                    break

            #Interpolate missing values
            if prevPos != -1 and nextPos != -1:
                prevVal = float(outputData[prevPos]["tmax"])
                nextVal = float(outputData[nextPos]["tmax"])
                outputData[i]["tmax"] = str((prevVal + nextVal) / 2)
            elif prevPos != -1:
                outputData[i]["tmax"] = outputData[prevPos]["tmax"]
            elif nextPos != -1:
                outputData[i]["tmax"] = outputData[nextPos]["tmax"]
    

    #Find positions with valid tmin values
    validTminPositions = []
    for i in range(len(outputData)):
        if outputData[i]["tmin"] != "NA":
            validTminPositions.append(i)
    
    #Fill in missing tmin values
    for i in range(len(outputData)):
        if outputData[i]["tmin"] == "NA":
            prevPos = -1
            nextPos = -1
            
            #Find previous and next valid positions
            for pos in validTminPositions:
                if pos < i:
                    prevPos = pos
                elif pos > i:
                    nextPos = pos
                    break
            
            #Interpolate missing values with proper formatting
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
    
    #Create final formatted results
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
                
                if(len(tokens) !=8):
                    print("We've no Idea why It Throws an error!!!")
                    continue

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

        #Check if we have enough cities for this region
        if(len(cities) < 3):
            outputSelected = {}
            return outputSelected
        
        #LOOP CITY until we get 3 random cities
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
        
        #Map city names to data files
        for cityLine in inputCities:
            tokens = cityLine.split(",")

            if len(tokens) != 8:
                continue

            if tokens[0] == "Region":
                continue

            fileName = tokens[5]
            cityName = tokens[1]
            state = tokens[2]
            
            cityFullName = f"{cityName} {state}"
            if cityFullName in cities:
                filePath = DATA_PATH + "/" + fileName
                cityFiles[cityFullName] = filePath
        
        #Process data for each city and store in dict
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
        
        #Generate all dates in range
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
        
        #Prepare output file with temperature averages
        outputLines = ["Date,Temperature"]
        
        for date in allDates:
            tmaxSum = 0
            tminSum = 0
            validCities = 0
            
            #Calculate average temperature across cities for this date
            for city, data in cityData.items():
                if date in data:
                    tmaxSum += data[date]["tmax"]
                    tminSum += data[date]["tmin"]
                    validCities += 1
            
            if validCities > 0:
                avgHigh = tmaxSum / validCities
                avgLow = tminSum / validCities
                
                #Calculate daily average in Fahrenheit
                dailyAvgF = (avgHigh + avgLow) / 2
                
                #Convert to Celsius
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
        
        #Process each region file
        for region in range(1, 10):
            regionFile = f"./data/outputs/{region}region.csv"
            
            try:
                regionData = readIntoList(regionFile)
                
                #Extract data and add region number
                for i in range(1, len(regionData)):
                    line = regionData[i]
                    
                    #Skip header if found
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
        
        #Write consolidated data
        writeListToFile(consolidatedLines, fileName)
        print(f"Regions consolidated to {fileName}")
        return True
        
    except Exception as e:
        print(f"Error consolidating regions: {e}")
        return False


def annual_means_per_region(regions, years, consolidatedFile):
    plt.rcParams["figure.figsize"] = [10, 6]
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)
    
    output_dir = "./data/charts"
    
    #Generate chart for each region
    for region in regions:
        regionName = f"Region{region}"
        yearsList = []
        tempsList = []
        
        #Calculate annual average for each year
        for year in years:
            yearlyTemps = helper.get_yearly_temperatures(regionName, year)
            
            #Filter out None values
            validTemps = []
            for temp in yearlyTemps:
                if temp is not None:
                    validTemps.append(temp)
            
            #Calculate and store yearly average if data exists
            if len(validTemps) > 0:
                total = 0
                for temp in validTemps:
                    total += temp
                average = total / len(validTemps)
                
                yearsList.append(year)
                tempsList.append(average)
            
        #Plot the data if available
        if len(yearsList) > 0:
            plt.figure()
            plt.plot(yearsList, tempsList, 'o-', linewidth=2)
            plt.xlabel('Year')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Annual Mean Temperatures for {regionName}')
            plt.grid(True)
            plt.savefig(f"{output_dir}/Annual Means - {regionName}.png")
            plt.close()


def annual_means_combined(regions, years, patterns, consolidatedFile):
    plt.rcParams["figure.figsize"] = [10, 6]
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)
    
    output_dir = "./data/charts"
    
    #Create single combined chart
    plt.figure()
    
    #Process each region with different pattern
    for i, region in enumerate(regions):
        regionName = f"Region{region}"
        yearsList = []
        tempsList = []
        
        #Calculate annual average for each year
        for year in years:
            yearlyTemps = helper.get_yearly_temperatures(regionName, year)
            
            #Filter out None values
            validTemps = []
            for temp in yearlyTemps:
                if temp is not None:
                    validTemps.append(temp)
            
            #Calculate and store yearly average if data exists
            if len(validTemps) > 0:
                total = 0
                for temp in validTemps:
                    total += temp
                average = total / len(validTemps)
                
                yearsList.append(year)
                tempsList.append(average)
        
        #Plot region data with cyclic pattern styles
        if len(yearsList) > 0:
            patternIndex = i % len(patterns)
            pattern = patterns[patternIndex]
            
            plt.plot(yearsList, tempsList, pattern, linewidth=2, label=regionName)
    
    #Add chart details and save
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.title('Annual Mean Temperatures for All Regions')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{output_dir}/Annual Means - All Regions.png")
    plt.close()


def single_day_per_region(regions, years, month, day, consolidatedFile):
    
    plt.rcParams["figure.figsize"] = [10, 6]
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)
    
    output_dir = "./data/charts"
    
    #Get month name for chart title
    date = datetime.date(2000, month, 1)
    monthName = date.strftime('%B')
    
    #Generate chart for each region
    for region in regions:
        regionName = f"Region{region}"
        yearsList = []
        tempsList = []
        
        #Get temperature for specific day each year
        for year in years:
            temp = helper.get_daily_temperature(regionName, year, month, day)
            if temp is not None:
                yearsList.append(year)
                tempsList.append(temp)
        
        #Create chart if data exists
        if len(yearsList) > 0:
            plt.figure()
            plt.plot(yearsList, tempsList, 'o-', linewidth=2)
            plt.xlabel('Year')
            plt.ylabel('Temperature (°C)')
            plt.title(f'Temperature on {monthName} {day} for {regionName}')
            plt.grid(True)
            plt.savefig(f"{output_dir}/{monthName} {day} - {regionName}.png")
            plt.close()


def single_day_combined(regions, years, month, day, patterns, consolidatedFile):
    
    plt.rcParams["figure.figsize"] = [10, 6]
    helper = TemperatureHelper.TemperatureHelper(consolidatedFile)
    
    output_dir = "./data/charts"
    
    #Get month name for chart title
    date = datetime.date(2000, month, 1)
    monthName = date.strftime('%B')
    
    #Create single combined chart
    plt.figure()
    
    #Process each region with different pattern
    for i, region in enumerate(regions):
        regionName = f"Region{region}"
        yearsList = []
        tempsList = []
        
        #Get temperature for specific day each year
        for year in years:
            temp = helper.get_daily_temperature(regionName, year, month, day)
            if temp is not None:
                yearsList.append(year)
                tempsList.append(temp)
        
        #Plot region data with cyclic pattern styles
        if len(yearsList) > 0:
        
            patternIndex = i % len(patterns)
            pattern = patterns[patternIndex]
            
            plt.plot(yearsList, tempsList, pattern, linewidth=2, label=regionName)
    
    #Add chart details and save
    plt.xlabel('Year')
    plt.ylabel('Temperature (°C)')
    plt.title(f'Temperature on {monthName} {day} for All Regions')
    plt.grid(True)
    plt.legend()
    plt.savefig(f"{output_dir}/{monthName} {day} - All Regions.png")
    plt.close()

if __name__ == "__main__":
    
    #Handle command line arguments
    if len(sys.argv) == 3:
        try:
            startYear = int(sys.argv[1])
            endYear = int(sys.argv[2])
            #Get 3 random cities for each region and create regional files
            dictionary = get_three_random_cities_per_region(startYear,endYear)
            for x,y in sorted(dictionary.items()):
                outPutfile= "./data/outputs/"+ str(x) +"region.csv"
                cities = y
                create_regional_file(cities,startYear,endYear,outPutfile)
        except ValueError:
            print("Error: Start year and end year must be integers")
    elif len(sys.argv) == 2:
        #Consolidate regional files into one
        fileName = sys.argv[1]
        consolidate_regions(fileName)
    else:
        #Show usage instructions
        print()
        print("Usage: python a4functions.py <start_year> <end_year>")
        print("Example: python a4functions.py 1994 2023")
        print()
        print("Or For Consolidation -->")
        print()
        print("python a4functions.py <file_name>")
        print("python a4functions.py consolidated")