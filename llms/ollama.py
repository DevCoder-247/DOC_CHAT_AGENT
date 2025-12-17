from langchain_community.llms import Ollama

llm = Ollama(
    # model="deepseek-r1:latest",
    model="gemma3:1b",
    base_url="http://localhost:11434",
    temperature=0.2,
)

def get_llm():
    return llm