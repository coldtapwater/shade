import os
import subprocess
import sys
import requests
import json
from colorama import Fore, Style

# From main.py's generate_response function
def generate_response(prompt, stream=False):
    OLLAMA_API_URL = "http://localhost:11434/api/generate"
    MODEL_NAME = "llama3.2:1b"

    try:
        data = {
            "model": MODEL_NAME,
            "prompt": prompt,
            "stream": stream
        }
        response = requests.post(OLLAMA_API_URL, json=data, stream=stream)
        if response.status_code == 200:
            if stream:
                content = ""
                for line in response.iter_lines(decode_unicode=True):
                    if line:
                        content += json.loads(line)['response']
                # Debugging: Print the content
                # print(f"\nDebug: AI Model Response:\n{content}")
                return content
            else:
                json_response = response.json()
                # Debugging: Print the JSON response
                # print(f"\nDebug: AI Model Response JSON:\n{json_response}")
                return json_response.get('response', '')
        else:
            print(f"Error: Received status code {response.status_code} from Ollama API")
            return None
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

def execute_system_command(system_action, output):
    action = system_action['action']
    target = system_action['target']

    if action == 'open_app':
        app_path = f"/Applications/{target}.app"
        if os.path.exists(app_path):
            confirmation = input(f"Do you want to open {target}? (y/n): ")
            if confirmation.lower() == 'y':
                subprocess.run(['open', app_path])
                print(f"{Fore.CYAN}{target} opened successfully.{Style.RESET_ALL}")

                # Optionally, copy output to the application (requires AppleScript)
                copy_to_app = input(f"Do you want to paste the output into {target}? (y/n): ")
                if copy_to_app.lower() == 'y':
                    # Copy the output to the clipboard
                    os.system(f"echo '{output}' | pbcopy")

                    # Automate pasting into a new document using AppleScript
                    if target == "TextEdit":
                        paste_text_in_textedit(output)
                    elif target == "Pages":
                        paste_text_in_pages(output)
                    elif target == "Microsoft Word":
                        paste_text_in_word(output)
                    else:
                        print(f"{Fore.RED}Automated pasting not supported for {target}.{Style.RESET_ALL}")

                else:
                    print(f"{Fore.CYAN}Output copied to clipboard. Paste it manually into {target}.{Style.RESET_ALL}")
            else:
                print(f"{Fore.CYAN}Operation cancelled.{Style.RESET_ALL}")
        else:
            print(f"{Fore.RED}Application {target} not found.{Style.RESET_ALL}")
    elif action == 'create_file':
        confirmation = input(f"Do you want to create a file named {target}? (y/n): ")
        if confirmation.lower() == 'y':
            try:
                with open(target, 'w') as f:
                    f.write(output)
                print(f"{Fore.CYAN}File {target} created with the output.{Style.RESET_ALL}")
            except Exception as e:
                print(f"{Fore.RED}Failed to create file: {e}{Style.RESET_ALL}")
        else:
            print(f"{Fore.CYAN}Operation cancelled.{Style.RESET_ALL}")
    # Add more actions as needed with proper safeguards

def paste_text_in_textedit(output):
    """
    Use AppleScript to automate opening a new document in TextEdit and pasting the text.
    """
    applescript = f'''
    tell application "TextEdit"
        activate
        delay 1
        make new document
        set the text of the front document to "{output}"
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
    print(f"{Fore.CYAN}Text pasted into a new TextEdit document.{Style.RESET_ALL}")

def paste_text_in_pages(output):
    """
    Use AppleScript to automate opening a new document in Pages and pasting the text.
    """
    applescript = f'''
    tell application "Pages"
        activate
        delay 1
        make new document
        tell the front document to set body text to "{output}"
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
    print(f"{Fore.CYAN}Text pasted into a new Pages document.{Style.RESET_ALL}")

def paste_text_in_word(output):
    """
    Use AppleScript to automate opening a new document in Microsoft Word and pasting the text.
    """
    applescript = f'''
    tell application "Microsoft Word"
        activate
        delay 1
        make new document
        set content of text object of active document to "{output}"
    end tell
    '''
    subprocess.run(['osascript', '-e', applescript])
    print(f"{Fore.CYAN}Text pasted into a new Word document.{Style.RESET_ALL}")