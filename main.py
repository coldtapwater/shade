import shades.usepackages as usepackages
from shades.generator import generator
from shades.data_sorter import data_sorter
from shades.file_mover import file_mover

def simple_classify(user_input):
    keywords = {
        "generate": "text_generator",
        "create": "text_generator",
        "write": "text_generator",
        "sort": "data_sorter",
        "order": "data_sorter",
        "arrange": "data_sorter",
        "move": "file_mover",
        "copy": "file_mover",
        "transfer": "file_mover"
    }
    
    user_input = user_input.lower()
    for keyword, tool in keywords.items():
        if keyword in user_input:
            return tool
    return "text_generator"  # default tool

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
    tool_name = simple_classify(user_input)
    result = execute_tool(tool_name, user_input)
    return result

def main():
    usepackages.usepackages()
    print("Welcome to the Modular AI System!")
    print("You can ask for text generation, data sorting, or file moving.")
    print("Examples:")
    print("- Generate a short story about a robot")
    print("- Sort these numbers: 5, 2, 8, 1, 9")
    print("- Move file.txt to folder/newfile.txt")
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
