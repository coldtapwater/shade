import ollama

llm = ollama.Client() 

def generate_response(model, prompt):
    res = llm.generate(
                model=model, 
                prompt=prompt)
    return res.get('response')

    

if __name__ == "__main__":
    print(generate_response("llama3.2:1b", "What is the meaning of life?"))