import shades.usepackages as usepackages
import router

def main():
    usepackages.usepackages()
    print("Welcome to the Modular AI System!")
    print("You can ask for various tasks, including:")
    print("- Text generation")
    print("- Data sorting")
    print("- File moving")
    print("- File creation")
    print("You can also combine multiple actions in a single request.")
    print("Examples:")
    print("- Generate a short story about a robot")
    print("- Sort these numbers: 5, 2, 8, 1, 9")
    print("- Create a file named 'test.txt' with content 'Hello, world!' and move it to '/Users/documents'")
    print("Type 'exit' to quit.")
    print()

    while True:
        user_input = input("Enter your request: ")
        if user_input.lower() == 'exit':
            break
        result = router.route(user_input)
        print(f"Result: {result}")
        print()

if __name__ == "__main__":
    main()
