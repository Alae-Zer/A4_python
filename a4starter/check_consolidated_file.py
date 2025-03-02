import sys
from FileUtils import readIntoList

def countLeapYears(startYear, endYear):
   #Count leap years in the given range
   leapYears = 0
   for year in range(startYear, endYear + 1):
       if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
           leapYears += 1
   return leapYears

def checkConsolidatedFile(filePath, startYear, endYear):
   try:
       #Read file and count lines
       lines = readIntoList(filePath)
       
       #Subtract header line
       actualLines = len(lines) - 1
       
       #Calculate expected lines based on years and leap years
       totalYears = endYear - startYear + 1
       leapYears = countLeapYears(startYear, endYear)
       normalYears = totalYears - leapYears
       
       #Total expected lines (days × regions)
       expectedLines = ((365 * normalYears) + (366 * leapYears)) * 9
       
       #Print file statistics
       print(f"Consolidated file: {filePath}")
       print(f"Years range: {startYear} to {endYear} ({totalYears} years)")
       print(f"Number of normal years: {normalYears}")
       print(f"Number of leap years: {leapYears}")
       print(f"Expected number of lines: {expectedLines}")
       print(f"Actual number of lines: {actualLines}")
       
       #Check if file has correct number of lines
       if actualLines == expectedLines:
           print("✓ File is complete!")
           return True
       else:
           print("✗ File is incomplete or has extra lines.")
           missingLines = expectedLines - actualLines
           if missingLines > 0:
               print(f"  Missing {missingLines} lines")
           else:
               print(f"  Has {abs(missingLines)} extra lines")
           return False
       
   except Exception as e:
       print(f"Error checking file: {e}")
       return False

if __name__ == "__main__":
   #Check command line arguments
   if len(sys.argv) != 4:
       print("Usage: python check_consolidated_file.py <consolidated_file_name> <start_year> <end_year>")
       print("Example: python check_consolidated_file.py consolidated.csv 1954 2023")
       sys.exit(1)
   
   fileName = sys.argv[1]
   filePath = f"data/outputs/{fileName}"
   
   try:
       #Parse year arguments and check file
       startYear = int(sys.argv[2])
       endYear = int(sys.argv[3])
       checkConsolidatedFile(filePath, startYear, endYear)
   except ValueError:
       print("Error: Start year and end year must be integers")
       sys.exit(1)