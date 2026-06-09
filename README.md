# AI-Powered Email Automation System

An AI-powered email automation system built using LangGraph, FastAPI, Gmail API, PostgreSQL, and Groq. The system automatically processes incoming emails, classifies customer intent, retrieves conversation history, generates context-aware responses, and supports human approval before sending replies.

## Features

- Automated email retrieval and processing using Gmail API
- Email intent classification using LLMs
- Context-aware response generation
- Conversation history retrieval from PostgreSQL
- Human approval workflow using LangGraph interrupts and resume
- Email history tracking and persistence
- REST APIs built with FastAPI
- Stateful workflow orchestration using LangGraph

## Workflow

```text
Incoming Email
      ↓
Intent Classification
      ↓
Retrieve Email History
      ↓
Generate AI Response
      ↓
Human Review (Optional)
      ↓
Send Reply
      ↓
Store Email History
```

## Tech Stack

### Backend
- Python
- FastAPI

### AI & Agent Framework
- LangGraph
- LangChain
- Groq 

### Database
- PostgreSQL
- SQLAlchemy

### Integrations
- Gmail API

## Project Structure

```text
app/
├── agent/
│   ├── graph.py
│   └── state.py
├── gmail/
│   ├── get_gmail_service.py
│   ├── get_mail.py
│   ├── send_mail.py
│   └── extract_email.py
├── router/
│   └── gmail_router.py
├── services/
│   ├── email_agent_service.py
│   └── llm_service.py
├── app.py
├── config.py
├── crud.py
├── database.py
├── main.py
├── models.py
└── schemas.py
```

## Core Components

### Email Processing
Retrieves incoming emails from Gmail and extracts sender, subject, thread ID, and content.

### Intent Classification
Analyzes email content to identify customer intent, urgency, and topic.

### Conversation History Retrieval
Fetches previous interactions from PostgreSQL to provide context for response generation.

### Response Generation
Generates personalized and context-aware email replies using Gemini.

### Human Review Workflow
Uses LangGraph interrupts and resume functionality to pause execution for approval or editing before sending responses.

### Email Delivery
Sends approved responses through Gmail while maintaining conversation threading.

## API Endpoints

### Process Latest Email

```http
POST /agent/process-latest
```

### Review Generated Response

```http
POST /agent/review
```

### Send Email

```http
POST /agent/send
```

## Getting Started

### Clone the Repository

```bash
git clone <repository-url>
cd EmailAgent
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Run the Application

```bash
uvicorn app.main:app --reload
```

Access the API documentation at:

```text
http://localhost:8000/docs
```

## Future Improvements

- Persistent LangGraph checkpoints using PostgresSaver
- React-based dashboard
- Multi-user support
- Email analytics and monitoring
- Cloud deployment

## Author

**Maneesh Anchan B**
