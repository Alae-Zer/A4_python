import os
import a4functions

def main():
    regions = list(range(1, 10))
    years = list(range(1954, 2023))
    
    consolidatedFile = "./data/outputs/consolidated.csv"
    
    patterns = ['r-o', 'g-s', 'b-^', 'c-v', 'm-<', 'y->', 'k-p', 'r--', 'g--']
    
    days = [
        (1, 4),
        (4, 9),
        (9, 13),
        (11, 7)
    ]
    
    outputFolder = "./data/charts"
    
    if not os.path.exists(outputFolder):
        os.makedirs(outputFolder)
    
    for month, day in days:
        a4functions.single_day_per_region(regions, years, month, day, consolidatedFile, outputFolder)
        
        a4functions.single_day_combined(regions, years, month, day, patterns, consolidatedFile, outputFolder)
    
    a4functions.annual_means_per_region(regions, years, consolidatedFile, outputFolder)
    a4functions.annual_means_combined(regions, years, patterns, consolidatedFile, outputFolder)
    
    print("All charts have been created in the 'charts' directory!")

if __name__ == "__main__":
    main()