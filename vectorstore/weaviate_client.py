import weaviate
from langchain_community.vectorstores import Weaviate
from langchain_community.embeddings import OllamaEmbeddings

WEAVIATE_URL = "http://localhost:8080"

_client = None
_embeddings = None
_vectorstore = None

def get_embeddings():
    global _embeddings
    if _embeddings is None:
        _embeddings = OllamaEmbeddings(
            model="nomic-embed-text",
            base_url="http://localhost:11434",
        )
    return _embeddings

def get_vectorstore():
    global _client, _vectorstore

    if _vectorstore:
        return _vectorstore

    _client = weaviate.Client(WEAVIATE_URL)

    _vectorstore = Weaviate(
        client=_client,
        index_name="DocumentChunk",
        text_key="text",
        embedding=get_embeddings(),
    )

    return _vectorstore


# def clear_vectorstore():
#     client = _client
#     client.schema.delete_class("DocumentChunk")


def clear_vectorstore():
    client = weaviate.Client("http://localhost:8080")

    class_name = "DocumentChunk"

    if client.schema.exists(class_name):
        client.schema.delete_class(class_name)
        print("Weaviate class deleted")

    # Recreate schema
    client.schema.create_class({
        "class": class_name,
        "vectorizer": "none",
        "properties": [
            {"name": "text", "dataType": ["text"]},
            {"name": "source", "dataType": ["text"]},
        ],
    })

    print("Weaviate class recreated")


