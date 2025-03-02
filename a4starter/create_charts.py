import os
import a4functions
import datetime

def main():
    # Configuration
    regions = list(range(1, 10))  # Regions 1-9
    consolidatedFile = "./data/outputs/consolidated.csv"
    
    # Define the years for which data is available
    # Update this range according to your data
    years = list(range(1954, 2023))
    
    # Define patterns for the combined charts
    patterns = ['r-o', 'g-s', 'b-^', 'c-v', 'm-<', 'y->', 'k-p', 'r--', 'g--']
    
    # Define the four days spaced throughout the year
    days = [
        (2, 3),    # February 3
        (5, 6),    # May 6
        (8, 9),    # August 9
        (11, 12)   # November 12
    ]
    
    # Create charts directory if it doesn't exist
    charts_dir = "./charts"
    if not os.path.exists(charts_dir):
        os.makedirs(charts_dir)
    
    # Create single day charts for each region
    for month, day in days:
        # Generate per-region charts
        a4functions.single_day_per_region(regions, years, month, day, consolidatedFile, charts_dir)
        
        # Generate combined chart for all regions
        a4functions.single_day_combined(regions, years, month, day, patterns, consolidatedFile, charts_dir)
    
    # Create annual mean charts
    a4functions.annual_means_per_region(regions, years, consolidatedFile, charts_dir)
    a4functions.annual_means_combined(regions, years, patterns, consolidatedFile, charts_dir)
    
    print("All charts have been created in the 'charts' directory!")

if __name__ == "__main__":
    main()