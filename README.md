
# 🧠 Intelligent Document Chat Agent

### Hybrid Vector + Graph RAG

**(Weaviate · NebulaGraph · LangGraph · Ollama · Streamlit)**

---

## 📌 Overview

The **Intelligent Document Chat Agent** implements a **true Hybrid Retrieval-Augmented Generation (RAG)** architecture by combining **semantic vector search** with **graph-based retrieval**, fully powered by **local infrastructure**.

The system supports **document ingestion, chunking, embedding, graph storage, hybrid retrieval, and answer generation**, all orchestrated using **LangGraph** and served via a **Streamlit UI**.

### Core Technologies

* **Vector Search** → Weaviate
* **Graph-Based Retrieval** → NebulaGraph
* **Workflow Orchestration** → LangGraph
* **Local LLMs & Embeddings** → Ollama
* **User Interface** → Streamlit

---

## 🏗️ High-Level Architecture

### Hybrid Retrieval Strategy

#### 🔹 Vector Retrieval (Weaviate)

* Semantic similarity search
* Embeddings generated using **Ollama**

#### 🔹 Graph Retrieval (NebulaGraph)

* Relationship-based retrieval using:

```
Document ── HAS_CHUNK ──▶ Chunk
```

#### 🔹 Hybrid Reranking

* Results from **Weaviate** and **NebulaGraph** are merged
* Final context is passed to the LLM for answer generation

---

## ⚙️ System Requirements (STRICT)

### Operating System

* Windows 10 / 11
* Linux / macOS (commands largely similar)

### Software Requirements

| Component      | Version / Notes                          |
| -------------- | ---------------------------------------- |
| Python         | **3.12.x (mandatory)**                   |
| Docker Desktop | Latest stable                            |
| Ollama         | Latest                                   |
| RAM            | **16 GB minimum** (DeepSeek-R1 is heavy) |
| Disk Space     | ~15 GB free                              |

---

## 📁 Project Folder Structure

```
doc-chat-agent/
│── app.py
│── .env
│── requirements.txt
│
├── agent/
│   ├── graph.py
│   ├── nodes.py
│   └── state.py
│
├── ingestion/
│   ├── loaders.py
│   └── chunker.py
│
├── vectorstore/
│   └── weaviate_client.py
│
├── graphdb/
│   └── nebula_client.py
│
├── llms/
│   └── ollama.py
│
└── venv/
```

---

## 🐍 Python Environment Setup

> **Follow this order strictly**

### 1️⃣ Create Virtual Environment

```bash
python -m venv venv
```

### 2️⃣ Activate Virtual Environment (Windows)

```bash
venv\Scripts\activate
```

### 3️⃣ Upgrade pip

```bash
python -m pip install --upgrade pip
```

### 4️⃣ Install Dependencies

```bash
pip install -r requirements.txt
```

---

## 🐳 Docker Services Setup

> **Critical startup sequence**

---

### 5.1 Start Weaviate (Vector Database)

#### First-Time Run

```bash
docker run -d --name weaviate -p 8080:8080 -e QUERY_DEFAULTS_LIMIT=25 -e AUTHENTICATION_ANONYMOUS_ACCESS_ENABLED=true -e DEFAULT_VECTORIZER_MODULE=none semitechnologies/weaviate:1.24.7
```

#### Subsequent Runs

```bash
docker start weaviate
```

#### Verify

```
http://localhost:8080/v1
```

---

### 5.2 Start NebulaGraph (Graph Database)

#### Clone (One-Time)

```bash
git clone https://github.com/vesoft-inc/nebula-docker-compose.git
cd nebula-docker-compose
```

#### Start Services

```bash
docker compose up -d
```

---

### 5.3 Start Nebula Studio (Graph UI)

#### First-Time

```bash
docker run -d --name nebula-studio -p 7001:7001 vesoft/nebula-graph-studio:nightly
```

#### Later Runs

```bash
docker start nebula-studio
```

#### Access UI

```
http://localhost:7001/welcome
```

#### Login Credentials

| Field    | Value                    |
| -------- | ------------------------ |
| Host     | **host.docker.internal** |
| Port     | 9669                     |
| Username | root                     |
| Password | nebula                   |
| Space    | doc_graph                |

> ❌ `localhost` will **NOT** work
> ✅ `host.docker.internal` is **mandatory**

---

## 🤖 Ollama Setup (LLM + Embeddings)

### Verify Ollama

```bash
ollama list
```

### Pull Required Models

```bash
ollama pull nomic-embed-text
ollama pull deepseek-r1
```

### Optional (Faster Model)

```bash
ollama pull gemma3:1b
```

### Run Model (PowerShell)

```bash
ollama run gemma3:1b
```

Ollama runs at:

```
http://localhost:11434
```

---

## 🚀 Running the Application

### Ensure All Services Are Running

* ✅ Weaviate (Docker)
* ✅ NebulaGraph (Docker Compose)
* ✅ Nebula Studio
* ✅ Ollama
* ✅ Python Virtual Environment

### Start Streamlit App

```bash
streamlit run app.py
```

### Open in Browser

```
http://localhost:8501
```

---

## 🔄 End-to-End Project Flow

1. Upload PDF / DOCX
2. Text extraction
3. Chunking
4. Embedding via Ollama
5. Store vectors in Weaviate
6. Store metadata in NebulaGraph
7. User query received
8. Vector + Graph retrieval
9. Hybrid reranking
10. LLM generates final answer

---

## 🧩 NebulaGraph Schema

### Tags

```
Document(doc_id, title)
Chunk(chunk_id, text)
```

### Edge

```
HAS_CHUNK (Document → Chunk)
```

---

## 🔍 Verification Queries

```ngql
SHOW SPACES;
USE doc_graph;

SHOW TAGS;
SHOW EDGES;

MATCH (d:Document) RETURN d LIMIT 5;
MATCH (c:Chunk) RETURN c LIMIT 5;

MATCH (d:Document)-[e:HAS_CHUNK]->(c:Chunk)
RETURN d, e, c LIMIT 5;
```

⚠️ **Important**

```ngql
RETURN d, c;     -- ❌ Will NOT visualize
RETURN d, e, c; -- ✅ Correct
```

---

## 🧪 Example Graph RAG Query

```ngql
MATCH (d:Document)-[e:HAS_CHUNK]->(c:Chunk)
WHERE c.text CONTAINS "CONTACT"
RETURN d, e, c;
```

---

## 🛠️ Common Issues & Fixes

| Issue                     | Fix                                  |
| ------------------------- | ------------------------------------ |
| Weaviate `nearText` error | Disable vectorizer, use `nearVector` |
| Empty graph               | Ensure `RETURN d, e, c`              |
| Streamlit upload bug      | Preserve file suffix                 |
| LangGraph key collision   | Use noun-based state keys            |
| LangSmith 403 error       | Set `LANGCHAIN_TRACING_V2=false`     |

---

## 🧹 Clean Shutdown / Termination

### Stop Streamlit

```
CTRL + C
```

### Stop Ollama

```bash
ollama stop deepseek-r1
# or
ollama stop gemma3:1b
```

### Stop All Docker Containers

```bash
docker stop $(docker ps -q)
```

### Optional: Remove Containers

```bash
docker rm -f $(docker ps -a -q)
```

---

## 🔐 Environment Variables (`.env`)

Create `.env` in the project root.

```env
# OPTIONAL: Gemini / Google APIs
GEMINI_API_KEY=
GOOGLE_API_KEY=

# OPTIONAL: LangSmith Tracing
LANGCHAIN_TRACING_V2=true
LANGCHAIN_API_KEY=
LANGCHAIN_PROJECT=doc-chat-agent
```

### Notes

* Gemini / Google keys are **NOT required**
* Project runs **fully locally using Ollama**
* Disable tracing if errors occur:

```env
LANGCHAIN_TRACING_V2=false
```

---

## 🚫 `.gitignore` (IMPORTANT)

```gitignore
.env
```

---

## 🔮 Future Enhancements

* Graph-based reasoning paths
* Advanced hybrid reranking
* Streaming responses
* Citation-aware answers
* Full Docker Compose stack
* Authentication & multi-user support

---

### ✅ This README is **GitHub-ready, professional, and portfolio-grade**

If you want next:

* 📄 **README → Word DOC**
* 🧱 **Architecture diagram**
* 🐳 **Single docker-compose.yml**
* 🧪 **Test cases section**

Just say the word 🚀
