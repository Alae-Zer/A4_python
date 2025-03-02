import numpy as np
import datetime
from FileUtils import readIntoList  

class TemperatureHelper:
   
   def __init__(self, consolidatedFile):
       self.data = {}
       self.load_data(consolidatedFile)
       
   def load_data(self, filename):
       try:
           lines = readIntoList(filename)
           
           #Process each line from consolidated file
           for line in lines:
               tokens = line.strip().split(',')
               
               #Skip header row
               if tokens[0] == "Region" and tokens[1] == "Date":
                   continue
               
               #Extract and store temperature data
               if len(tokens) == 3:
                   
                   region = "Region" + tokens[0]
                   dateParts = tokens[1].split('-') 
                   year = int(dateParts[0])
                   month = int(dateParts[1])
                   day = int(dateParts[2])
                   
                   temperature = float(tokens[2])
                   
                   #Build nested dictionary structure for data access
                   regionDict = self.data 
                   if region not in regionDict:
                       regionDict[region] = {}
                   
                   yearDict = regionDict[region]
                   if year not in yearDict:
                       yearDict[year] = {}
                   
                   monthDict = yearDict[year]
                   if month not in monthDict:
                       monthDict[month] = {}
                   
                   monthDict[day] = temperature
       except FileNotFoundError:
           print(f"Error: Could not find file {filename}")
       except Exception as e:
           print(f"Error loading data: {e}")

   def get_daily_temperature(self, region, year, month, day):
       try:
           #Validate date is correct
           datetime.date(year, month, day)
           
           #Navigate through nested dictionary to find temperature
           regionDict = self.data
           if region not in regionDict:
               return None
           
           yearDict = regionDict[region]
           if year not in yearDict:
               return None
           
           monthDict = yearDict[year]
           if month not in monthDict:
               return None
           
           if day not in monthDict:
               return None
           
           return monthDict[day]
           
       except ValueError:
           print(f"Error: Invalid date {year}-{month}-{day}")
           return None

   def get_yearly_temperatures(self, region, year):
       temperatures = []
       
       #Return empty array if region or year not in data
       if region not in self.data:
           return np.array(temperatures)
       if year not in self.data[region]:
           return np.array(temperatures)
       
       #Set date range for entire year
       startDate = datetime.date(year, 1, 1)
       endDate = datetime.date(year, 12, 31)
       
       #Loop through each day of the year
       currentDate = startDate
       while currentDate <= endDate:
           month = currentDate.month
           day = currentDate.day
           
           #Get temperature data if available
           regionDict = self.data
           yearDict = regionDict[region]
           monthDict = yearDict[year]
           
           if month in monthDict and day in monthDict:
               temp = monthDict[day]
               temperatures.append(temp)
           else:
               temperatures.append(None)
           
           #Move to next day
           currentDate += datetime.timedelta(days=1)
       
       return np.array(temperatures)