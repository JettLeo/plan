# Excel Agent · AI Multi-Agent Collaboration System

> Built with LangGraph, featuring Supervisor + Workers multi-agent architecture, Excel parsing/validation/generation, RAG knowledge retrieval, and Checkpoint persistence.

---

## 📌 Project Overview

This is a hands-on **AI Agent development project** — a complete implementation from a Java backend engineer transitioning to AI Agent development. It demonstrates:

- **Supervisor + Workers multi-agent collaboration**
- **Excel parsing, validation, and JSON generation**
- **RAG (Retrieval-Augmented Generation) with ChromaDB + FAQ knowledge base**
- **Checkpoint state persistence (resumable execution)**
- **Enterprise-grade Python practices** (type hints, logging, configuration management)

---

## 🛠️ Tech Stack

| Category | Technology |
| :--- | :--- |
| Language | Python 3.10+ |
| Agent Framework | LangGraph |
| Web Framework | FastAPI |
| Vector Database | ChromaDB |
| State Persistence | SQLite (Checkpoint) |
| Data Processing | Pandas, OpenPyXL |
| Configuration | Pydantic Settings, python-dotenv |
| Logging | logging |
| Package Management | pyproject.toml |

---

## 📁 Project Structure

```text
excel-agent/
├── app/                         # Main application module
│   ├── agents/                  # Agent definitions
│   │   └── multi_agent.py       # Main Agent (Supervisor + 5 Workers)
│   ├── core/                    # Core configuration
│   │   └── config.py            # Unified configuration management
│   └── rag/                     # RAG module
│       ├── __init__.py
│       └── vector_store.py      # ChromaDB vector store wrapper
├── data/                        # Data directory
│   └── faq.xlsx                 # FAQ knowledge base sample
├── scripts/                     # Utility scripts
│   ├── generate_faq.py          # Generate FAQ sample data
│   ├── load_faq_data.py         # Load FAQ into vector store
│   └── create_sample_excel.py   # Create sample Excel file
├── tests/                       # Test scripts
│   └── test_retrieve.py         # Retrieval test
├── .env                         # Environment variables (not committed)
├── .gitignore
├── pyproject.toml               # Project dependencies
└── README.md