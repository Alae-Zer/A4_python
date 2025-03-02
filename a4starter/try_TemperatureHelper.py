from TemperatureHelper import TemperatureHelper

def main():
   
   #Create helper with consolidated file
   helper = TemperatureHelper("./data/outputs/consolidated.csv")
   
   #Test get_daily_temperature method with various cases
   print("Testing get_daily_temperature method:")
   print(f"Temperature for Region1, 1954-01-01: {helper.get_daily_temperature('Region1', 1954, 1, 1)}")
   print(f"Temperature for Region1, 1954-01-10: {helper.get_daily_temperature('Region1', 1954, 1, 10)}")
   print(f"Temperature for Region2, 1954-01-01: {helper.get_daily_temperature('Region2', 1954, 1, 1)}")
   
   print(f"Testing with invalid date: {helper.get_daily_temperature('Region1', 1954, 2, 30)}")
   
   #Test get_yearly_temperatures method
   print("\nTesting get_yearly_temperatures method:")
   tempsRegion1_1954 = helper.get_yearly_temperatures('Region1', 1954)
   if len(tempsRegion1_1954) > 0:
       print(f"First 10 temperatures for Region1, 1954: {tempsRegion1_1954[:10]}")
       
       #Calculate average temperature from valid values
       validTemps = [t for t in tempsRegion1_1954 if t is not None]
       if validTemps:
           avgTemp = sum(validTemps) / len(validTemps)
           print(f"Average temperature for Region1, 1954: {avgTemp:.2f}")
   
   #Compare with another region
   tempsRegion2_1954 = helper.get_yearly_temperatures('Region2', 1954)
   if len(tempsRegion2_1954) > 0:
       validTemps = [t for t in tempsRegion2_1954 if t is not None]
       if validTemps:
           avgTemp = sum(validTemps) / len(validTemps)
           print(f"Average temperature for Region2, 1954: {avgTemp:.2f}")
   
   print(f"Number of days in Region1, 1954: {len(tempsRegion1_1954)}")
   
   #Test with leap year
   tempsLeapYear = helper.get_yearly_temperatures('Region1', 1956)
   if len(tempsLeapYear) > 0:
       print(f"Number of days in leap year (1956): {len(tempsLeapYear)}")

if __name__ == "__main__":
   main()