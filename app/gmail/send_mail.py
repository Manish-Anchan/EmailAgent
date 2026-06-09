from .get_gmail_service import get_gmail_service
import base64
from email.mime.text import MIMEText

def send_reply(email, subject, body, thread_id):
    service = get_gmail_service()

    message = MIMEText(body)

    message["to"] = email
    message["subject"] = f"Re: {subject}"

    raw = base64.urlsafe_b64encode(
        message.as_bytes()
    ).decode()

    service.users().messages().send(
        userId="me",
        body={
            "raw": raw,
            "threadId": thread_id
        }
    ).execute()