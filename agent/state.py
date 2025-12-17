from typing import List
from langchain.schema import Document
from typing_extensions import TypedDict

class AgentState(TypedDict):
    docs: List[Document]
    chunks: List[Document]
    query: str
    vector_results: List[str]
    graph_results: List[str]
    answer: str
