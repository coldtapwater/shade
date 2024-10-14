import re

def sort_data(input_string):
    # Extract numbers from the input string
    numbers = re.findall(r'\d+', input_string)
    
    # Convert strings to integers and sort
    sorted_numbers = sorted(map(int, numbers))
    
    # Convert back to strings and join with commas
    result = ", ".join(map(str, sorted_numbers))
    
    return f"Sorted data: {result}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        input_string = sys.argv[1]
        print(sort_data(input_string))
    else:
        print("Please provide a string of numbers to sort.")
