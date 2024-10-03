import requests
import json
import sys
import re
import time
import threading
import subprocess
import os
import readline  # For better input experience on macOS

from colorama import Fore, Style, init
from agents import PlanningAgent, CheckingAgent, CraftingAgent, ConfidenceAgent, SystemAgent
from tools import execute_system_command
from memory import ConversationManager

# Initialize colorama
init(autoreset=True)

OLLAMA_API_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "llama3.2:1b"

def generate_response(prompt, stream=False):
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
                return content
            else:
                return response.json()['response']
        else:
            print(f"Error: Received status code {response.status_code} from Ollama API")
            return None
    except Exception as e:
        print(f"Error generating response: {str(e)}")
        return None

def parse_response(response):
    # Debugging: Print the response before parsing
    # print(f"\nDebug: Response Before Parsing:\n{response}")

    thinking_pattern = r'\[THINKING\](.*?)\s*(?=\[SHADING\]|\[OUTPUT\]|$)'
    shading_pattern = r'\[SHADING\](.*?)\s*(?=\[THINKING\]|\[OUTPUT\]|$)'
    output_pattern = r'\[OUTPUT\](.*)'

    thinking_matches = re.findall(thinking_pattern, response, re.DOTALL)
    shading_matches = re.findall(shading_pattern, response, re.DOTALL)
    output_match = re.search(output_pattern, response, re.DOTALL)

    thinking = [match.strip() for match in thinking_matches]
    shading = [match.strip() for match in shading_matches]
    output = output_match.group(1).strip() if output_match else ""


    return thinking, shading, output

def type_effect(text, color):
    for char in text:
        sys.stdout.write(color + char + Style.RESET_ALL)
        sys.stdout.flush()
        time.sleep(0.02)  # Adjust typing speed here
    print()  # Newline after typing effect

def chain_of_thought_prompt(user_input):
    # Agents handle different parts of the reasoning
    conversation = ConversationManager(max_tokens=128000)
    planning_agent = PlanningAgent()
    checking_agent = CheckingAgent()
    crafting_agent = CraftingAgent()
    confidence_agent = ConfidenceAgent()
    system_agent = SystemAgent()

    # Planning agent generates the initial plan
    plan = planning_agent.plan(user_input, conversation.get_context())

    # Extract and display the [THINKING] section immediately
    thinking, _, _ = parse_response(plan)
    if thinking:
        print(f"\n{Fore.YELLOW}[THINKING]{Style.RESET_ALL}")
        for thought in thinking:
            type_effect(thought, Fore.YELLOW)

    # Checker agent reviews the plan
    shaded_plan = checking_agent.check_plan(plan, user_input, conversation.get_context())

    # Extract and display the [SHADING] section immediately
    _, shading, _ = parse_response(shaded_plan)
    if shading:
        print(f"\n{Fore.BLUE}[SHADING]{Style.RESET_ALL}")
        for shade in shading:
            type_effect(shade, Fore.BLUE)

    # Crafting agent generates the response based on the refined plan
    response = crafting_agent.craft_response(shaded_plan, user_input, conversation.get_context())

    # Confidence agent evaluates the response
    confidence = confidence_agent.evaluate_response(response, user_input)

    # Regenerate response if confidence is below threshold
    max_attempts = 3
    attempts = 1
    while confidence < 0.9 and attempts < max_attempts:
        # For simplicity, we won't re-display the thinking and shading sections
        plan = planning_agent.plan(user_input)
        shaded_plan = checking_agent.check_plan(plan, user_input)
        response = crafting_agent.craft_response(shaded_plan, user_input)
        confidence = confidence_agent.evaluate_response(response, user_input)
        attempts += 1

    # System agent decides if any system action is needed
    system_action = system_agent.decide_action(user_input, response)

    return response, system_action

def main():
    print(f"{Fore.CYAN}ShadeAI{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Using model: {MODEL_NAME}{Style.RESET_ALL}")
    print(f"{Fore.CYAN}Type 'exit' to quit the app.{Style.RESET_ALL}\n")

    while True:
        try:
            user_input = input(f"{Fore.MAGENTA}Enter your prompt: {Style.RESET_ALL}")

            if user_input.lower() == 'exit':
                print(f"{Fore.CYAN}Thank you for using ShadeAI{Style.RESET_ALL}")
                break

            print(f"\n{Fore.YELLOW}Generating response...{Style.RESET_ALL}")

            full_response, system_action = chain_of_thought_prompt(user_input)

            # Parse and display the [OUTPUT] section
            _, _, output = parse_response(full_response)
            print(f"\n{Fore.GREEN}[OUTPUT]{Style.RESET_ALL}")
            type_effect(output, Fore.GREEN)

            # Execute system command if applicable
            if system_action:
                execute_system_command(system_action, output)
        except KeyboardInterrupt:
            print(f"\n{Fore.CYAN}Thank you for using ShadeAI{Style.RESET_ALL}")
            break

if __name__ == "__main__":
    main()