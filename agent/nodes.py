from ingestion.chunker import chunk_docs
from vectorstore.weaviate_client import get_vectorstore
# from graphdb.nebula_client import create_doc_node
# from llms.gemini import get_llm
from llms.ollama import get_llm
from vectorstore.weaviate_client import get_vectorstore, get_embeddings

from graphdb.nebula_client import insert_document, insert_chunk
import uuid

from vectorstore.weaviate_client import get_vectorstore, get_embeddings
from graphdb.nebula_client import graph_search_keywords


llm = get_llm()

vectorstore = get_vectorstore()
embeddings = get_embeddings()

def chunk_node(state):
    state["chunks"] = chunk_docs(state["docs"])
    return state

def embed_node(state):
    vectorstore.add_documents(state["chunks"])
    return state

# def graph_node(state):
#     for d in state["docs"]:
#         create_doc_node(d.metadata.get("source", "doc"), "Uploaded Document")
#     return state
def graph_node(state):
    for chunk in state["chunks"]:
        doc_id = chunk.metadata.get("source", "doc")

        insert_document(doc_id, doc_id)

        chunk_id = str(uuid.uuid4())
        insert_chunk(doc_id, chunk_id, chunk.page_content)

    return state


# def query_node(state):
#     query = state["query"]
#     query_vector = embeddings.embed_query(query)

#     docs = vectorstore.similarity_search_by_vector(query_vector, k=3)

#     contents = []
#     total_chars = 0
#     for d in docs:
#         if total_chars > 2000:
#             break
#         contents.append(d.page_content)
#         total_chars += len(d.page_content)

#     state["vector_results"] = contents or ["No relevant context found."]
#     return state


def query_node(state):
    query = state["query"]

    # --- Vector search ---
    q_vector = embeddings.embed_query(query)
    v_docs = vectorstore.similarity_search_by_vector(q_vector, k=5)
    vector_results = [d.page_content for d in v_docs]

    # --- Graph search ---
    # keywords = query.lower().split()[:5]
    STOPWORDS = {"what", "is", "the", "a", "an", "of", "in", "on", "for", "and"}

    # keywords = [
    #     w for w in query.lower().split()
    #     if w not in STOPWORDS and len(w) > 3
    # ][:5]
    keywords = [w for w in query.lower().split()]
    graph_results = graph_search_keywords(keywords, limit=10)

    state["vector_results"] = vector_results
    state["graph_results"] = graph_results
    print("KEYWORDS:", keywords)
    print("GRAPH RESULTS:", graph_results[:2])

    return state



def hybrid_rerank(vector_results, graph_results):
    scores = {}

    for text in vector_results:
        scores[text] = scores.get(text, 0) + 2.0

    for item in graph_results:
        text = item if isinstance(item, str) else item[0]
        scores[text] = scores.get(text, 0) + 1.0

    ranked = sorted(scores.items(), key=lambda x: x[1], reverse=True)
    return [text for text, _ in ranked][:5]




# def answer_node(state):
#     context = "\n".join(state["vector_results"])

#     prompt = f"""
# You are an intelligent document assistant.

# Use ONLY the context below to answer.

# Context:
# {context}

# Question:
# {state['query']}

# Answer clearly and concisely.
# """

#     response = llm.invoke(prompt)   # ✅ returns string
#     state["answer"] = response
#     return state


def answer_node(state):
    combined = hybrid_rerank(
        state.get("vector_results", []),
        state.get("graph_results", [])
    )

    print("VECTOR:", state["vector_results"][:2])
    print("GRAPH:", state["graph_results"][:2])


    context = "\n\n".join(combined[:3])

    response = llm.invoke(
        f"""
Answer using ONLY the context below.

Context:
{context}

Question:
{state['query']}
"""
    )

    state["answer"] = response
    return state
