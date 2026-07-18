from typing import TypedDict, Literal


class EmailClassification(TypedDict):
    intent: Literal["question", "bug", "billing", "feature", "complex", "notification"]
    urgency: Literal["low", "medium", "high", "critical"]
    topic: str
    summary: str


class EmailAgentState(TypedDict):
    user_id: str          
    email_content: str
    sender_email: str
    email_id: str
    subject: str

    classification: EmailClassification | None

    search_results: list[str] | None
    customer_history: dict | None

    draft_response: str | None
    messages: list[str] | None