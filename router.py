import ollama
import json
import re
from shades.generator import generator
from shades.data_sorter import data_sorter
from shades.file_mover import file_mover

# Initialize Ollama client
ollama_client = ollama.Client()

def select_tools(user_input):
    prompt = f"""
    Given the following user input, determine the appropriate tool(s) to use and the order in which they should be applied. Available tools are:
    1. text_generator: Generates text based on a prompt
    2. data_sorter: Sorts numerical data
    3. file_mover: Moves files from one location to another
    4. file_writer: Creates a new file with specified content

    User input: {user_input}

    Respond with a list of tools and their inputs, one per line, in the following format:
    tool: input
    
    For example:
    file_writer: Create a file named 'example.txt' with content 'Hello, world!'
    file_mover: Move 'example.txt' to '/Users/documents'
    """

    response = ollama_client.generate(model="llama3.2:1b", prompt=prompt)
    response_text = response['response']
    
    tools = []
    for line in response_text.split('\n'):
        if ':' in line:
            tool, input_text = line.split(':', 1)
            tools.append({"tool": tool.strip(), "input": input_text.strip()})
    
    if not tools:
        print("Error: Could not parse tool selection from Llama model")
        # Fallback: use a simple keyword-based selection
        if "sort" in user_input.lower():
            tools = [{"tool": "data_sorter", "input": user_input}]
        elif "move" in user_input.lower() or "copy" in user_input.lower():
            tools = [{"tool": "file_mover", "input": user_input}]
        elif "create" in user_input.lower() or "write" in user_input.lower():
            tools = [{"tool": "file_writer", "input": user_input}]
        else:
            tools = [{"tool": "text_generator", "input": user_input}]
    
    return tools

def execute_tool(tool, input_text):
    if tool == "text_generator":
        return generator.generate_response("llama3.2:1b", input_text)
    elif tool == "data_sorter":
        return data_sorter.sort_data(input_text)
    elif tool == "file_mover":
        return file_mover.move_file(input_text)
    elif tool == "file_writer":
        return file_writer(input_text)
    else:
        return f"Unknown tool: {tool}"

def file_writer(input_text):
    # Extract file name and content from input
    match = re.search(r"Create a file named '(.+)' with content '(.+)'", input_text)
    if not match:
        return "Invalid input for file_writer"
    file_name, content = match.groups()

    try:
        with open(file_name, 'w') as f:
            f.write(content)
        return f"File '{file_name}' created successfully"
    except Exception as e:
        return f"Error creating file: {str(e)}"

def route(user_input):
    tools = select_tools(user_input)
    results = []
    for tool_info in tools:
        tool = tool_info['tool']
        input_text = tool_info['input']
        result = execute_tool(tool, input_text)
        results.append(result)
    return " | ".join(results)

if __name__ == "__main__":
    # Test the router
    test_input = "Create a file named 'test.txt' with content 'Hello, world!' and move it to '/Users/documents'"
    result = route(test_input)
    print(result)
