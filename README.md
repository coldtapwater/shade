# shadeai

welcome to **shadeAI**! This application leverages advanced AI reasoning to generate dynamic responses, integrating chain-of-thought reasoning with agent-based architecture and macOS system-level interactions. It's designed to provide an interactive and intelligent terminal experience, showcasing features such as streaming outputs, context-aware conversations, and automated system actions.

---

## table of contents

- [Features](#features)
- [Architecture Overview](#architecture-overview)
  - [Main Components](#main-components)
  - [Agents](#agents)
  - [Tools](#tools)
  - [Memory Management](#memory-management)
- [Installation and Setup](#installation-and-setup)
- [Usage](#usage)
  - [Running the Application](#running-the-application)
  - [Interacting with the App](#interacting-with-the-app)
  - [Example Scenarios](#example-scenarios)
- [Security Considerations](#security-considerations)
- [Future Enhancements](#future-enhancements)
- [License](#license)

---

## features

- **dynamic terminal responses**: The app streams AI-generated responses character by character, providing a typing effect for `[THINKING]`, `[SHADING]`, and `[OUTPUT]` sections.
- **chain-of-thought reasoning with Agents**: Utilizes multiple agents to simulate advanced reasoning processes, including planning, checking, crafting, and evaluating responses.
- **macos system-level interactions**: Integrates with macOS to perform actions like opening applications, managing files, and automating tasks through AppleScript.
- **memory management**: Implements a conversation manager with a context window of up to 128k tokens, summarizing older messages to maintain context within limits.
- **user safeguards**: Includes prompts for user confirmations before executing any system-level commands to ensure security and prevent unauthorized actions.

---

## architecture overview

### main components

1. **`main.py`**: The entry point of the application. It handles user input, coordinates the agents, displays dynamic outputs, and manages system interactions.
2. **`agents.py`**: Contains the agent classes responsible for different aspects of reasoning, including planning, checking, crafting, and system actions.
3. **`tools.py`**: Provides utility functions for system-level interactions, such as executing commands, opening applications, and automating tasks with AppleScript.
4. **`memory.py`**: Manages the conversation history and context window, ensuring the AI has access to relevant information while respecting token limits.

### agents

The application uses an agent-based architecture to simulate a chain-of-thought reasoning process:

- **planner**: Breaks down the user's request into detailed steps and decides how to approach it.
- **shader**: Reviews and refines the plan to ensure it aligns with the user's intent.
- **crafter**: Generates the final response based on the refined plan.
- **confidence**: Evaluates the response and determines confidence levels. [COMING SOON]
- **interaction**: Decides if any system-level actions are needed based on the user's request and the response.

### tools

The `tools.py` module provides functionalities for:

- **system commands execution**: Safely executing system-level commands with user confirmation.
- **application automation**: Opening applications and automating tasks using AppleScript (e.g., pasting text into a new document).
- **response generation**: Interacting with the Ollama API to generate AI responses.

### memory management

The `ConversationManager` in `memory.py`:

- **context window**: Maintains a conversation history with a maximum of 128k tokens.
- **token counting**: Tracks token usage to prevent exceeding limits.
- **summarization**: Summarizes older conversation parts to free up tokens when limits are reached. [COMING SOON]

---

## installation and setup

### prerequisites

- **Python 3.x**
- **macOS**: The system interaction features are designed for macOS.
- **Ollama API**: Ensure the Ollama API is running and accessible at `http://localhost:11434/api/generate`.

### install required packages

Open your terminal and run:

```bash
pip install requests colorama
```

### clone the repository

```bash
git clone https://github.com/coldtapwater/shade.git
cd shade
```

## usage

### running the application

Navigate to the project directory and run:

```bash
python main.py
```

### Interacting with the App

- **enter prompts**: Type your requests or questions when prompted.
- **exit**: Type `exit` to quit the application.

### example scenarios

#### writing a story

**user input**:

```
I want to write a story about a duck in a pond who has the most amazing friends.
```

**expected behavior**:

1. **[THINKING]**: The app displays the AI's thought process in real-time, breaking down the request.
2. **[SHADING]**: Shows refinements and considerations.
3. **[OUTPUT]**: Provides the final story.
4. **System Action**: Offers to open a text editor and automatically paste the story into a new document.

#### explaining a Concept

**user input**:

```
Explain how photosynthesis works in plants.
```

**expected behavior**:

1. **[THINKING]**: AI outlines key points about photosynthesis.
2. **[SHADING]**: Refines the explanation for clarity.
3. **[OUTPUT]**: Delivers a comprehensive explanation.

---

## security considerations

- **user confirmation**: The app prompts for user confirmation before executing any system-level actions.
- **application checks**: Verifies the existence of applications before attempting to open them.
- **limited actions**: Only predefined and safe system commands are allowed.
- **no unauthorized actions**: The app includes safeguards to prevent unintended system modifications.

---

## future enhancements

- **enhanced summarization**: Implement AI-based summarization for better memory management.
- **additional tools**: Expand system interaction capabilities, such as web navigation or advanced file management.
- **cross-platform support**: Adapt system-level features for other operating systems. [FAR IN THE FUTURE]
- **Iimproved AI integration**: Enhance the AI model's ability to follow instructions and handle complex prompts.

---

## License

This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---

**note**: This application is intended for educational and experimental purposes. Always exercise caution when executing system-level commands and ensure you understand the implications of the actions being performed.

Feel free to contribute to the project or suggest improvements!
