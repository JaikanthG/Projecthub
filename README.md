# Project Hub 📊

> **Enterprise Engineering Knowledge and Productivity Platform**

Project Hub is an all-in-one software lifecycle management and collaboration platform that unifies project tracking, engineering knowledge bases, bug and task workflows, Root Cause Analysis (RCA) post-mortems, document management, and an AI-driven contextual RAG assistant.

---

## 🚀 Getting Started & Run Commands

### 1. Prerequisites
- **Python**: 3.10+ (Recommended: 3.11 / 3.12 / 3.13)
- **PostgreSQL**: With `pgvector` extension enabled
- **Ollama**: (Optional for local embeddings: `ollama pull nomic-embed-text`)
- **Groq API Key**: (For Project Hub AI Agent)

---

### 2. Activate the Virtual Environment

Before starting either service, activate the project virtual environment:

#### Windows (PowerShell)
```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned
& e:\Project_Hub\myenv\Scripts\Activate.ps1
```

#### macOS / Linux
```bash
source myenv/bin/activate
```

---

### 3. Run the Backend (FastAPI)

The backend provides the RESTful API, authentication, RBAC, and AI services.

Open a terminal, activate your virtual environment, and run:

```powershell
# From the project root (E:\Project_Hub)
python -m uvicorn Project_Management.main:app --reload --port 3000
```

- **API Base URL**: [http://127.0.0.1:3000](http://127.0.0.1:3000)
- **Swagger Interactive API Documentation**: [http://127.0.0.1:3000/docs](http://127.0.0.1:3000/docs)
- **ReDoc Documentation**: [http://127.0.0.1:3000/redoc](http://127.0.0.1:3000/redoc)

---

### 4. Run the Frontend (Streamlit)

The frontend provides the complete web dashboard and UI.

Open a **separate terminal**, activate your virtual environment, and run:

```powershell
cd E:\Project_Hub\Project_Hub_Frontend
streamlit run app.py
```

- **Web Application URL**: [http://localhost:8501](http://localhost:8501)

---

## 🛠️ Tech Stack

| Layer | Technologies |
| :--- | :--- |
| **Backend** | FastAPI, Uvicorn, SQLAlchemy 2.0, Pydantic v2 |
| **Frontend** | Streamlit, Requests, PyJWT |
| **Database & Vector Store** | PostgreSQL, `pgvector`, Psycopg |
| **AI & RAG Pipeline** | Agno Agent Framework, Groq (`gpt-oss-120b`), Ollama (`nomic-embed-text` - 768d) |
| **Authentication & Security** | JWT (python-jose), Passlib (bcrypt), Role-Based Access Control (RBAC) |

---

## 📦 Key Features

- **🔐 Multi-Tier RBAC & Security**: System roles (`admin`, `employee`) + granular project-level permissions (`admin`, `contributor`, `member`, `viewer`).
- **📁 Project Workspace Management**: Organize software projects with technology stacks, description, and team assignments.
- **📚 Knowledge Base & Automated RAG**: Publish engineering documentation with instant chunking and vector indexing into `pgvector`.
- **🤖 Project Hub AI Agent**: Contextual AI assistant with hybrid vector search, strict project-isolated boundaries, and anti-hallucination guardrails.
- **🐞 Bug & Task Tracking**: Full lifecycle management with priorities, assignees, and status pipelines (`todo`, `in_progress`, `done`).
- **🧾 Root Cause Analysis (RCA)**: Structured post-mortem engineering reports linked directly to resolved bugs.
- **📄 Document Storage**: Secure project document uploads and downloads.
- **🔔 Activity Log & Notifications**: Real-time project audit history and user notifications.

---

## ⚙️ Environment Configuration (`.env`)

Create a `.env` file in `Project_Management/` with your configuration:

```env
# Database
DATABASE_URL=postgresql+psycopg://postgres:<PASSWORD>@localhost:5432/project_management

# Security / JWT
SECRET_KEY=<YOUR_STRONG_SECRET_KEY>
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1440

# AI Configuration
GROQ_API_KEY=<YOUR_GROQ_API_KEY>
```

---

## 📝 Git Workflow

To commit and push updates to GitHub:

```powershell
cd E:\Project_Hub
git add README.md
git commit -m "docs: add project documentation and run commands to README"
git push origin main
```
