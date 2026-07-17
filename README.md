# ✉️ Email Agent — AI-Powered Email Automation

An intelligent email automation system that processes incoming Gmail messages using an AI agent pipeline. Built with **LangGraph**, **FastAPI**, **Streamlit**, **PostgreSQL**, and **Groq (Llama 3.3)**, the system classifies customer intent, retrieves conversation history, generates context-aware draft replies, and supports human-in-the-loop approval before sending.

---

## ✨ Features

- **Automated Email Ingestion** — Fetches the latest unread email from Gmail via the Gmail API.
- **LLM-Powered Intent Classification** — Categorises emails by intent (`question`, `bug`, `billing`, `feature`, `complex`, `notification`) and urgency (`low` → `critical`) using structured output.
- **Conditional Routing** — LangGraph `Command`-based routing directs the workflow through bug tracking, history retrieval, or straight to human review depending on classification.
- **Conversation History** — Retrieves up to 5 previous emails from the same sender (PostgreSQL) to give the LLM historical context when drafting replies.
- **Context-Aware Response Generation** — Drafts professional, empathetic replies grounded in the email content, classification, and sender history.
- **Human-in-the-Loop Review** — Uses LangGraph `interrupt` / `resume` to pause the pipeline for human approval or rejection before any email is sent.
- **One-Click Send** — Approved replies are dispatched via the Gmail API, maintaining thread continuity.
- **Streamlit Dashboard** — A polished, dark-themed UI with a step-by-step wizard (Fetch → Review → Send) and real-time session state.

---

## 🔄 Agent Workflow

```
              ┌──────────────────┐
              │  Incoming Email   │
              └────────┬─────────┘
                       │
              ┌────────▼─────────┐
              │ Classify Intent   │
              │  (LLM Structured) │
              └────────┬─────────┘
                       │
          ┌────────────┼────────────┐
          │            │            │
   billing/critical    bug       other intents
          │            │            │
          ▼            ▼            ▼
   ┌────────────┐ ┌──────────┐ ┌──────────────────┐
   │Human Review│ │Bug Track │ │Fetch Email History│
   └────────────┘ └────┬─────┘ └────────┬─────────┘
                       │                │
                       ▼                ▼
                  ┌──────────────────────────┐
                  │    Draft Response (LLM)   │
                  └────────────┬─────────────┘
                               │
                     high urgency / complex?
                        ┌──────┴──────┐
                        │ yes         │ no
                        ▼             ▼
                 ┌────────────┐   ┌───────┐
                 │Human Review│   │  END  │
                 │ (interrupt)│   └───────┘
                 └──────┬─────┘
                        │ resume
                        ▼
                     ┌───────┐
                     │  END  │
                     └───────┘
```

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| **Frontend** | Streamlit |
| **Backend API** | FastAPI, Uvicorn |
| **Agent Framework** | LangGraph, LangChain |
| **LLM Provider** | Groq — `llama-3.3-70b-versatile` |
| **Database** | PostgreSQL, SQLAlchemy |
| **Email Integration** | Gmail API (OAuth 2.0) |
| **Config** | Pydantic Settings, `.env` |

---

## 📁 Project Structure

```
EmailAgent/
├── app/
│   ├── agent/
│   │   ├── graph.py                 # LangGraph workflow definition & compilation
│   │   ├── state.py                 # EmailAgentState & EmailClassification schemas
│   │   └── nodes/
│   │       ├── classify_intent.py   # LLM-based intent classification + routing
│   │       ├── email_history.py     # Fetch sender's previous emails from DB
│   │       ├── response_nodes.py    # Draft response generation + human review interrupt
│   │       └── search_and_track.py  # Bug ticket creation
│   ├── gmail/
│   │   ├── get_gmail_service.py     # Gmail API OAuth2 service builder
│   │   ├── get_mail.py              # Fetch latest unread email
│   │   ├── send_mail.py             # Send reply via Gmail
│   │   └── extract_email.py         # Extract email address from sender string
│   ├── router/
│   │   └── gmail_router.py          # FastAPI routes: /process-latest, /review, /send
│   ├── services/
│   │   ├── email_agent_service.py   # Orchestrates graph execution, review resume, send
│   │   └── llm_service.py           # Groq LLM instance factory
│   ├── app.py                       # Streamlit frontend (dashboard UI)
│   ├── config.py                    # Pydantic settings (env vars)
│   ├── crud.py                      # Database CRUD operations
│   ├── database.py                  # SQLAlchemy engine & session
│   ├── main.py                      # FastAPI app entry point
│   ├── models.py                    # SQLAlchemy ORM models (EmailHistory)
│   └── schemas.py                   # Pydantic request/response schemas
├── credentials.json                 # Gmail API OAuth credentials (gitignored)
├── token.pickle                     # Gmail OAuth token cache (gitignored)
├── requirements.txt
├── .env                             # Environment variables (gitignored)
└── .gitignore
```

---

## 🚀 Getting Started

### Prerequisites

- Python 3.11+
- PostgreSQL running locally
- A Google Cloud project with the Gmail API enabled and OAuth credentials downloaded as `credentials.json`
- A Groq API key

### 1. Clone the Repository

```bash
git clone https://github.com/Manish-Anchan/EmailAgent.git
cd EmailAgent
```

### 2. Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate        # Linux / macOS
# .venv\Scripts\activate         # Windows
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Up PostgreSQL

Create a database for the project:

```sql
CREATE DATABASE "EmailAgent";
```

> Tables are auto-created on first run via SQLAlchemy `create_all`.

### 5. Configure Environment Variables

Create a `.env` file in the project root:

```env
GROQ_API_KEY=your_groq_api_key
MODEL_NAME=llama-3.3-70b-versatile

DATABASE_HOSTNAME=localhost
DATABASE_PORT=5432
DATABASE_USERNAME=postgres
DATABASE_PASSWORD=your_password
DATABASE_NAME=EmailAgent
```

### 6. Set Up Gmail API Credentials

1. Go to the [Google Cloud Console](https://console.cloud.google.com/).
2. Enable the **Gmail API**.
3. Create OAuth 2.0 credentials (Desktop App).
4. Download the credentials file and save it as `credentials.json` in the project root.
5. On first run, a browser window will open for OAuth consent — this generates `token.pickle` for subsequent runs.

### 7. Run the Application

**Start the FastAPI backend:**

```bash
uvicorn app.main:app --reload
```

**Start the Streamlit frontend** (in a separate terminal):

```bash
streamlit run app/app.py
```

| Service | URL |
|---|---|
| FastAPI Docs (Swagger) | [http://localhost:8000/docs](http://localhost:8000/docs) |
| Streamlit Dashboard | [http://localhost:8501](http://localhost:8501) |

---

## 📡 API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| `GET` | `/` | Health check |
| `POST` | `/agent/process-latest` | Fetch the latest unread email and run the agent pipeline |
| `POST` | `/agent/review` | Submit human review decision (approve / reject) |
| `POST` | `/agent/send` | Send the approved draft reply via Gmail |

### Request Schemas

**`POST /agent/review`**

```json
{
  "thread_id": "string",
  "approved": true,
  "edited_response": "string or null"
}
```

**`POST /agent/send`**

```json
{
  "thread_id": "string"
}
```

---

## 🗄️ Database Schema

**`email_history`**

| Column | Type | Notes |
|---|---|---|
| `id` | UUID | Primary key (auto-generated) |
| `email_id` | VARCHAR(255) | Unique Gmail message ID |
| `thread_id` | VARCHAR(255) | Gmail thread ID |
| `sender_email` | VARCHAR(255) | Sender address |
| `recipient` | VARCHAR(255) | Recipient address |
| `subject` | TEXT | Email subject |
| `content` | TEXT | Email body |
| `direction` | VARCHAR(10) | `inbound` or `outbound` |
| `timestamp` | TIMESTAMP(tz) | Defaults to `now()` |

---

## 🔮 Future Improvements

- Persistent LangGraph checkpoints with PostgresSaver
- Multi-user / multi-inbox support
- Email analytics and monitoring dashboard
- Batch email processing
- Cloud deployment (Railway / Render / AWS)

---

## 👤 Author

**Manish Anchan**
