import numpy as np
import datetime
from FileUtils import readIntoList

class TemperatureHelper:
    def __init__(self, consolidatedFile):
        self.data = {}
        self._loadData(consolidatedFile)
    
    def _loadData(self, filename):
        try:
            lines = readIntoList(filename)
            
            for i in range(1, len(lines)):
                line = lines[i]
                parts = line.strip().split(',')
                if len(parts) == 3:
                    region = f"Region{parts[0]}"
                    dateParts = parts[1].split('-')
                    year = int(dateParts[0])
                    month = int(dateParts[1])
                    day = int(dateParts[2])
                    temperature = float(parts[2])
                    
                    if region not in self.data:
                        self.data[region] = {}
                    if year not in self.data[region]:
                        self.data[region][year] = {}
                    if month not in self.data[region][year]:
                        self.data[region][year][month] = {}
                    
                    self.data[region][year][month][day] = temperature
                    
        except FileNotFoundError:
            print(f"Error: Could not find file {filename}")
        except Exception as e:
            print(f"Error loading data: {e}")
    
    def get_daily_temperature(self, region, year, month, day):
        try:
            datetime.date(year, month, day)
            
            if region not in self.data:
                return None
            if year not in self.data[region]:
                return None
            if month not in self.data[region][year]:
                return None
            if day not in self.data[region][year][month]:
                return None
                
            return self.data[region][year][month][day]
                
        except ValueError:
            print(f"Error: Invalid date {year}-{month}-{day}")
            return None
    
    def get_yearly_temperatures(self, region, year):
        temperatures = []
        
        if region not in self.data:
            return np.array(temperatures)
        if year not in self.data[region]:
            return np.array(temperatures)
        
        startDate = datetime.date(year, 1, 1)
        endDate = datetime.date(year, 12, 31)
        
        currentDate = startDate
        while currentDate <= endDate:
            month = currentDate.month
            day = currentDate.day
            
            if month in self.data[region][year] and day in self.data[region][year][month]:
                temp = self.data[region][year][month][day]
                temperatures.append(temp)
            else:
                temperatures.append(None)
            
            currentDate += datetime.timedelta(days=1)
        
        return np.array(temperatures)