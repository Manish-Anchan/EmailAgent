from .get_gmail_service import composio_client


def send_reply(user_id: str, email: str, subject: str, body: str, thread_id: str):
    """
    Send a reply email through the authenticated user's Gmail account.

    Args:
        user_id:   Composio user identifier (same one used to connect Gmail)
        email:     Recipient email address
        subject:   Email subject (will be prefixed with "Re: ")
        body:      Plain-text email body
        thread_id: Gmail thread ID to reply in
    """
    try:
        result = composio_client.tools.execute(
            slug="GMAIL_SEND_EMAIL",
            arguments={
                "to": email,
                "subject": f"Re: {subject}",
                "body": body,
                "thread_id": thread_id,
            },
            user_id=user_id,
            version="20260702_01",
        )
    except Exception as e:
        raise Exception(f"Composio GMAIL_SEND_EMAIL failed: {e}")

    return result