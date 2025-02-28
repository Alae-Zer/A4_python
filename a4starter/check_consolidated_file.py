import sys
from FileUtils import readIntoList

def count_leap_years(start_year, end_year):
    """Count the number of leap years in the given range (inclusive)."""
    leap_years = 0
    for year in range(start_year, end_year + 1):
        if (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0):
            leap_years += 1
    return leap_years

def check_consolidated_file(file_path, start_year, end_year):
    """Check if the consolidated file has the expected number of lines."""
    try:
        
        lines = readIntoList(file_path)
        
        actual_lines = len(lines) - 1
        
        total_years = end_year - start_year + 1
        leap_years = count_leap_years(start_year, end_year)
        normal_years = total_years - leap_years
        
        expected_lines = ((365 * normal_years) + (366 * leap_years)) * 9
        
        print(f"Consolidated file: {file_path}")
        print(f"Years range: {start_year} to {end_year} ({total_years} years)")
        print(f"Number of normal years: {normal_years}")
        print(f"Number of leap years: {leap_years}")
        print(f"Expected number of lines: {expected_lines}")
        print(f"Actual number of lines: {actual_lines}")
        
        if actual_lines == expected_lines:
            print("✓ File is complete!")
            return True
        else:
            print("✗ File is incomplete or has extra lines.")
            missing_lines = expected_lines - actual_lines
            if missing_lines > 0:
                print(f"  Missing {missing_lines} lines")
            else:
                print(f"  Has {abs(missing_lines)} extra lines")
            return False
            
    except Exception as e:
        print(f"Error checking file: {e}")
        return False

if __name__ == "__main__":
    if len(sys.argv) != 4:
        print("Usage: python check_consolidated_file.py <consolidated_file> <start_year> <end_year>")
        print("Example: python check_consolidated_file.py ./data/outputs/consolidated.csv 1954 2023")
        sys.exit(1)
    
    file_path = sys.argv[1]
    try:
        start_year = int(sys.argv[2])
        end_year = int(sys.argv[3])
        check_consolidated_file(file_path, start_year, end_year)
    except ValueError:
        print("Error: Start year and end year must be integers")
        sys.exit(1)