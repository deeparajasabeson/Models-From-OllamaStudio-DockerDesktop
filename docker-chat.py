from openai import OpenAI
client = OpenAI(
    base_url="http://localhost:12434/engines/v1",
    api_key="YOUR_API_KEY"
)

print("Welcome to the Docker Chat! Type 'exit' to quit.")
while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        print("Exiting the chat. Goodbye!")
        break

    response = client.chat.completions.create(
        model="llama3.2",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": user_input}
        ]
    )

    assistant_reply = response.choices[0].message.content
    print(f"Bot: {assistant_reply}")