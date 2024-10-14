from transformers import pipeline, AutoTokenizer, AutoModelForSequenceClassification
import torch

def load_model():
    model_name = "distilbert-base-uncased-finetuned-sst-2-english"
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)
    return pipeline("text-classification", model=model, tokenizer=tokenizer)

def predict_tool(classifier, user_input):
    result = classifier(user_input)
    # For this example, we'll map the sentiment to tool names
    # In a real scenario, you'd train a model specifically for tool classification
    if result[0]['label'] == 'POSITIVE':
        return "text_generator"
    else:
        return "data_sorter"

def execute_tool(tool_name, user_input):
    if tool_name == "text_generator":
        return text_generator(user_input)
    elif tool_name == "data_sorter":
        return data_sorter(user_input)
    else:
        return f"Unknown tool: {tool_name}"

def text_generator(prompt):
    # Placeholder for text generation tool
    return f"Generated text based on: {prompt}"

def data_sorter(data):
    # Placeholder for data sorting tool
    return f"Sorted data: {data}"

def route(user_input):
    model = load_model()
    tool_name = predict_tool(model, user_input)
    result = execute_tool(tool_name, user_input)
    return result

if __name__ == "__main__":
    # Test the router
    test_input = "Generate a short story about a robot"
    result = route(test_input)
    print(result)
