import streamlit as st
import os
import tempfile
from dotenv import load_dotenv

from agent.graph import graph
from ingestion.loaders import load_document


from vectorstore.weaviate_client import clear_vectorstore
from graphdb.nebula_client import clear_graph

# for langsmith studio
os.environ["LANGCHAIN_TRACING_V2"] = "true"


# Load environment variables
load_dotenv()

st.title("📄 Intelligent Document Chat Agent")

# Upload
uploaded = st.file_uploader(
    "Upload Document",
    type=["pdf", "docx", "xlsx"]
)

# Query input
query = st.text_input("Ask a question")

if uploaded and query:
    # ✅ Preserve file extension
    suffix = os.path.splitext(uploaded.name)[1].lower()

    with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as f:
        f.write(uploaded.read())
        temp_path = f.name

    # Load document
    docs = load_document(temp_path)

    # Build LangGraph state
    state = {
        "docs": docs,
        "query": query
    }

    # Invoke graph
    result = graph.invoke(state)

    st.write("### Answer")
    st.write(result["answer"])

st.sidebar.title("⚙️ Controls")

if st.sidebar.button("🧹 Clear Memory"):
    clear_vectorstore()
    clear_graph()

    st.session_state.clear()

    st.success("Memory cleared. Previous PDFs forgotten.")
    st.experimental_rerun()