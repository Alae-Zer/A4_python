import a4functions

def main():
   
   #Define regions and years for temperature analysis
   regions = list(range(1, 10))
   years = list(range(1954, 2023))
   
   consolidatedFile = "./data/outputs/consolidated.csv"
   
   #Define line patterns for different regions in charts
   patterns = ['r-', 'g-', 'b-', 'c-', 'm-', 'y-', 'k-', 'r--', 'g--']
   
   #Specific days to analyze (month, day)
   days = [
       (1, 4),
       (4, 9),
       (9, 13),
       (11, 7)
   ]
   
   #Generate charts for specific days
   for month, day in days:
       a4functions.single_day_per_region(regions, years, month, day, consolidatedFile)
       a4functions.single_day_combined(regions, years, month, day, patterns, consolidatedFile)
   
   #Generate annual means charts
   a4functions.annual_means_per_region(regions, years, consolidatedFile)
   a4functions.annual_means_combined(regions, years, patterns, consolidatedFile)
   
   print("All charts have been created in the 'charts' directory!")

if __name__ == "__main__":
   main()