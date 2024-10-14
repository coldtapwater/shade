import os
import shutil
import re
import ollama

ollama_client = ollama.Client()

def extract_file_info(instruction):
    try:
        prompt = f"""
        Extract the file name and destination from the following instruction:
        Instruction: {instruction}
        
        Respond in the following format:
        File name: [extracted file name]
        Destination: [extracted destination]
        """
        
        response = ollama_client.generate(model="llama3.2:1b", prompt=prompt)
        generated_text = response['response']
        
        # Extract file name and destination from the generated text
        file_name_match = re.search(r"File name: (.+)", generated_text)
        destination_match = re.search(r"Destination: (.+)", generated_text)
        
        file_name = file_name_match.group(1).strip() if file_name_match else ""
        destination = destination_match.group(1).strip() if destination_match else ""
        
        if not file_name or not destination:
            raise ValueError("Failed to extract file name or destination")
        
        return file_name, destination
    except Exception as e:
        print(f"Error using Ollama model: {str(e)}. Falling back to regex-based extraction.")
        return regex_extract_file_info(instruction)

def regex_extract_file_info(instruction):
    file_match = re.search(r"'([^']+)'", instruction)
    file_name = file_match.group(1) if file_match else ""
    
    dir_match = re.search(r"'([^']+)'$", instruction)
    destination = dir_match.group(1) if dir_match else ""
    
    return file_name, destination

def move_file(instruction):
    print(f"Received instruction: {instruction}")
    
    file_name, destination = extract_file_info(instruction)
    
    if not file_name or not destination:
        return "Error: Could not extract file name and destination from the instruction."
    
    print(f"Extracted file name: '{file_name}', destination: '{destination}'")
    
    # Expand user directory if needed
    source = os.path.expanduser(file_name)
    destination = os.path.expanduser(destination)
    
    try:
        # Check if source file exists
        if not os.path.exists(source):
            return f"Error: Source file '{source}' does not exist."
        
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Move the file
        shutil.move(source, os.path.join(destination, os.path.basename(source)))
        return f"Successfully moved '{source}' to '{destination}'."
    except Exception as e:
        return f"An error occurred: {str(e)}"

if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1:
        instruction = " ".join(sys.argv[1:])
        print(move_file(instruction))
    else:
        print("Please provide a file moving instruction.")
