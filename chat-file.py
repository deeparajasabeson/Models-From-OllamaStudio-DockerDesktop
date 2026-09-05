# RAG based Setup
from ollama import chat
import fitz

MODEL_NAME = "llama3.2"
PDF_PATH = "data/Deepa-PythonAzureAIAgenticAIMCPDotNET.pdf"
print("Ollama RAG chat demo: type exit to quit")

def read_pdf_text(pdf_path):
    """Extract text from a PDF file."""
    text = ""
    with fitz.open(pdf_path) as pdf:
        for page in pdf:
            text += page.get_text()
    return text 

def chunk_text(text, chunk_size=1000):
    """Check if the text is too long and split it into chunks."""
    if len(text) > chunk_size:
        print(f"Text is too long ({len(text)} characters). Splitting into chunks of {chunk_size} characters.")
        return text[:chunk_size]
    return [text]

def find_relevant_chunks(question, chunks, top_k=3):
    """Find the most relevant chunks based on the question."""
    question_words = set(question.lower().split())
    scores = []
    for chunk in chunks:
        score = sum(
            1 for word in question_words if word in chunk.lower()
        )
        scores.append((score, chunk))

    scores.sort(reverse=True)
    return [chunk for score, chunk in scores[:top_k]]

print ("Reading PDF file...")
pdf_text = read_pdf_text(PDF_PATH)
chunks = chunk_text(pdf_text)

conversation=[]
print("PDF Agent is ready")
print("type exit to quit")
print("=" * 50)

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    relevant_chunks = find_relevant_chunks(user_input, chunks)
    context = "\n\n".join(relevant_chunks)

    system_message = """
    You are an Azure AI Tutor.

    Use the PDF context when relevant.
    
    If the answer is not found in the PDF, 
    use your general knowledge and clearly'
    mention that is outside the document.
    """

    conversation.append({"role": "system", "content": system_message})
    conversation.append({"role": "user", "content": f"Context:\n{context}\n\nQuestion:\n{user_input}"})

    response = chat(
        model = MODEL_NAME, 
        messages=conversation, 
        stream=True)

    full_response = ""
    for chunk in response:
        content = chunk["message"]["content"]
        full_response += content
        print(content, end="", flush=True)
            
    conversation.append({"role": "assistant", "content": full_response})
    print("\n" + "-" * 80)
