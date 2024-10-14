import os
import shutil

def move_file(instruction):
    # Parse the instruction to extract source and destination
    parts = instruction.split(" to ")
    if len(parts) != 2:
        return "Invalid instruction. Please use the format: 'Move [source] to [destination]'"
    
    source = parts[0].split("Move ")[-1].strip()
    destination = parts[1].strip()
    
    try:
        # Check if source file exists
        if not os.path.exists(source):
            return f"Error: Source file '{source}' does not exist."
        
        # Create destination directory if it doesn't exist
        os.makedirs(os.path.dirname(destination), exist_ok=True)
        
        # Move the file
        shutil.move(source, destination)
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
