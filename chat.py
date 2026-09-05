from ollama import chat

MODEL_NAME = "llama3.2"
print("Ollama chat demo: type exit to quit")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break
    response = chat(MODEL_NAME, messages=[{
        "role": "user", 
        "content": user_input
    }], stream=True)

    print(f"{MODEL_NAME}: {response}")
    for chunk in response:
        print(chunk['message']['content'], end="", flush=True)
    print()  # Print a newline after the streamed response





