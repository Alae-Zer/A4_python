import sys
from a4functions import create_regional_file, get_three_random_cities_per_region

if __name__ == "__main__":
    
    if len(sys.argv) == 3:
        try:
            startYear = int(sys.argv[1])
            endYear = int(sys.argv[2])
            dictionary = get_three_random_cities_per_region(startYear,endYear)

            accum = 0
            for x,y in sorted(dictionary.items()):
                outPutfile= "./data/outputs/"+ str(x) +"region.csv"
                cities = y
                if(create_regional_file(cities,startYear,endYear,outPutfile)):
                    accum +=1
                    print(f"{str(x)}region.csv has been created in data/outputs folder")

            print()
            print(f"Total {accum} files created")
        except ValueError:
            print("Error: Start year and end year must be integers")
    else:
        print("Usage: python create_regional_files.py <start_year> <end_year>")
        print("Example: python create_regional_files.py 1954 2023")