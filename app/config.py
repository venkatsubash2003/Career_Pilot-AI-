from langchain_ollama import ChatOllama

def get_llm():
    return ChatOllama(
        model="llama3.1",
        temperature=0
    )

def get_json_llm():
    return ChatOllama(
        model = "llama3.1",
        temperature = 0,
        format = "json"
    )