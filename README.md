# Enterprise Grade Agentic RAG System

An enterprise-grade Agentic Retrieval-Augmented Generation (RAG) system built with **LangGraph**, **FastAPI**, **Qdrant Vector Database**, **Google Gemini Embeddings**, and **Groq LLMs**.

## Features

- **Agentic Workflow with LangGraph**: State-driven architecture featuring planner, retriever, and responder nodes with built-in conversation memory checkpointing.
- **Enterprise Vector Search**: Scalable hybrid/vector indexing and search using Qdrant.
- **High-Performance LLMs & Embeddings**: Powered by Groq LLMs (e.g. `llama-3.3-70b-versatile`) with fallback support and Google Gemini embeddings.
- **Observability & Monitoring**: Deep tracing and logging with Logfire integration.
- **FastAPI REST API**: High-performance endpoints for question answering, state tracking, and Mermaid graph visualization.
- **Data Ingestion Pipeline**: Ingestion pipeline supporting document chunking, cleaning, and indexing into Qdrant collections.

## Project Structure

```text
EnterpriseGradeRAG/
├── app/
│   ├── agents/            # LangGraph workflow, state, and nodes (planner, retriever, responder)
│   ├── ingestion/         # Chunking, loaders, and data processing pipeline
│   ├── services/          # Retrieval and vector store integration (Qdrant, Gemini)
│   ├── config.py          # Centralized configuration & environment loader
│   └── main.py            # FastAPI application & REST endpoints
├── DATA/                  # Dataset samples & raw documents
├── images/                # Architecture diagrams & assets
├── ui/                    # User interface
├── .env.example           # Example environment configuration
├── requirements.txt       # Python dependencies
└── data_ingestion_commands.md # Data ingestion guide
```

## Setup & Installation

### 1. Clone the Repository
```bash
git clone https://github.com/pranav-4432/EnterpriseGradeRAG.git
cd EnterpriseGradeRAG
```

### 2. Create and Activate Virtual Environment
```bash
python -m venv .venv
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate
```

### 3. Install Dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables
Copy `.env.example` to `.env` and fill in your API credentials:
```bash
cp .env.example .env
```
Fill in the following variables:
- `GEMINI_API_KEY`: Your Google Gemini API Key
- `QDRANT_CLUSTER_ENDPOINT`: Your Qdrant Cloud or Local Endpoint
- `QDRANT_API_KEY`: Your Qdrant API Key
- `GROQ_API_KEY`: Your Groq API Key
- `GROQ_FALLBACK_API_KEY`: (Optional) Fallback Groq API Key
- `LOGFIRE_TOKEN`: (Optional) Pydantic Logfire Token

## Running the Application

### Start FastAPI Backend
```bash
uvicorn app.main:app --reload --port 8000
```
- API Docs: `http://localhost:8000/docs`
- Graph Visualization: `http://localhost:8000/graph`
- Health Check: `http://localhost:8000/`

### Data Ingestion
Refer to [`data_ingestion_commands.md`](data_ingestion_commands.md) for details on ingesting clean or noisy datasets into Qdrant.

```bash
# Ingest clean dataset
python -m app.ingestion.processor DATA/true_data true
```
