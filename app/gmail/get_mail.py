from .get_gmail_service import composio_client


def get_latest_email(user_id: str) -> dict | None:
    """
    Returns the most recent email from the user's inbox,
    or None if there are no emails.
    """
    try:
        result = composio_client.tools.execute(
            slug="GMAIL_FETCH_EMAILS",
            arguments={
                "query": "in:inbox",       
                "max_results": 1,
            },
            user_id=user_id,
            version="20260702_01",
        )
    except Exception as e:
        raise Exception(f"Composio GMAIL_FETCH_EMAILS failed: {e}")


    data = result if isinstance(result, dict) else {}

    if hasattr(result, 'data'):
        data = result.data if isinstance(result.data, dict) else {}
    elif hasattr(result, 'to_dict'):
        data = result.to_dict()

    messages = data.get("messages", []) or data.get("data", {}).get("messages", [])

    if not messages:
        return None


    msg = messages[0]

    sender  = msg.get("sender") or msg.get("from") or msg.get("From", "")
    subject = msg.get("subject") or msg.get("Subject", "")
    body    = msg.get("messageText") or msg.get("body") or msg.get("snippet") or msg.get("messageBody") or msg.get("preview", "")
    msg_id  = msg.get("id") or msg.get("messageId", "")
    thread_id = msg.get("threadId") or msg.get("thread_id") or msg_id

    print("Message ID:", msg_id)
    print("Thread ID:", thread_id)

    return {
        "id": msg_id,
        "sender": sender,
        "thread_id": thread_id,
        "subject": subject,
        "body": body,
    }