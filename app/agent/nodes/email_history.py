from typing import Literal
from langgraph.types import Command
from ..state import EmailAgentState
from app.models import EmailHistory
from sqlalchemy.orm import Session


def make_fetch_email_history(db):
    def fetch_email_history(
        state: EmailAgentState,
    ) -> Command[Literal["draft_response"]]:
        """Fetch previous emails from this sender to give the LLM historical context."""

        sender_email = state.get("sender_email", "").strip()

        if not sender_email:
            return Command(
                update={
                    "customer_history": {
                        "previous_emails": [],
                        "email_count": 0,
                        "sender_email": "",
                    }
                },
                goto="draft_response",
            )

        try:
            
            raw_emails = (
                    db.query(EmailHistory)
                    .filter(EmailHistory.sender_email.ilike(f"%{sender_email}%"))
                    .order_by(EmailHistory.timestamp.desc())
                    .limit(5)
                    .all()
                )

            previous_emails = []
            for email in raw_emails:
                if hasattr(email, 'content'):
                    content = email.content or ""
                    subject = email.subject or ""
                    timestamp = str(email.timestamp or "")
                else:
                    content = email.get("content", "") or ""
                    subject = email.get("subject", "")
                    timestamp = str(email.get("timestamp", ""))

                previous_emails.append(
                    {
                        "subject": subject,
                        "snippet": content[:600],
                        "timestamp": timestamp,
                    }
                )

            customer_history = {
                "previous_emails": previous_emails,
                "email_count": len(previous_emails),
                "sender_email": sender_email,
            }

        except Exception as e:
            customer_history = {
                "previous_emails": [],
                "email_count": 0,
                "sender_email": sender_email,
                "error": str(e),
            }

        return Command(
            update={"customer_history": customer_history},
            goto="draft_response",
        )

    return fetch_email_history
