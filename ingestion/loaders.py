from langchain_community.document_loaders import PyPDFLoader, Docx2txtLoader
from langchain.schema import Document
import pandas as pd
import os

def load_document(path: str):
    ext = os.path.splitext(path)[1].lower()

    if ext == ".pdf":
        return PyPDFLoader(path).load()

    if ext == ".docx":
        return Docx2txtLoader(path).load()

    if ext == ".xlsx":
        df = pd.read_excel(path)
        text = df.to_string(index=False)
        return [Document(page_content=text, metadata={"source": path})]

    raise ValueError(f"Unsupported file format: {ext}")
