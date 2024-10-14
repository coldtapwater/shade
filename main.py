import shades.usepackages as usepackages
from shades.generator import generator
from shades.data_sorter import data_sorter
from shades.file_mover import file_mover
import re
import os

def context_aware_classify(user_input):
    user_input = user_input.lower()
    
    # Check for file operations
    if re.search(r'\b(move|copy|transfer)\b.*\b(file|directory|folder)\b', user_input):
        return "file_mover"
    
    # Check for sorting operations
    if re.search(r'\b(sort|order|arrange)\b.*\d', user_input):
        return "data_sorter"
    
    # Default to text generation for any other input
    return "text_generator"

def preprocess_text_generator(user_input):
    # Remove any text generation related keywords
    keywords = ["generate", "create", "write"]
    for keyword in keywords:
        user_input = user_input.replace(keyword, "").strip()
    return user_input

def preprocess_data_sorter(user_input):
    # Extract numbers from the input
    numbers = re.findall(r'\d+', user_input)
    return ", ".join(numbers)

def execute_tool(tool_name, user_input):
    if tool_name == "text_generator":
        return generator.generate_response("llama3.2:1b", user_input)
    elif tool_name == "data_sorter":
        return data_sorter.sort_data(user_input)
    elif tool_name == "file_mover":
        return file_mover.move_file(user_input)
    else:
        return f"Unknown tool: {tool_name}"

def route(user_input):
    tool_name = context_aware_classify(user_input)
    
    if tool_name == "text_generator":
        preprocessed_input = preprocess_text_generator(user_input)
    elif tool_name == "data_sorter":
        preprocessed_input = preprocess_data_sorter(user_input)
    else:
        preprocessed_input = user_input
    
    result = execute_tool(tool_name, preprocessed_input)
    return result

def main():
    usepackages.usepackages()
    print("Welcome to the Modular AI System!")
    print("You can ask for text generation, data sorting, or file moving.")
    print("Examples:")
    print("- Generate a short story about a robot")
    print("- Sort these numbers: 5, 2, 8, 1, 9")
    print("- Can you move the file 'test.txt' into my directory '/Downloads'")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("Enter your request: ")
        if user_input.lower() == 'exit':
            break
        result = route(user_input)
        print(f"Result: {result}")
        print()

if __name__ == "__main__":
    main()
