from .get_gmail_service import get_gmail_service
import base64

def get_latest_email():
    service = get_gmail_service()

    results = service.users().messages().list(
        userId="me",
        labelIds=["INBOX"],
        maxResults=1
    ).execute()

    messages = results.get("messages", [])

    if not messages:
        return None

    msg_id = messages[0]["id"]
    try:
        msg_data = service.users().messages().get(
            userId="me",
            id=msg_id
        ).execute()
    except Exception as e:
        raise Exception(
            f"Unable to read email: {str(e)}"
        )
    print("Message ID:", msg_data["id"])
    print("Thread ID:", msg_data["threadId"])

    payload = msg_data["payload"]

    sender = ""
    subject = ""

    for h in payload["headers"]:
        if h["name"] == "From":
            sender = h["value"]

        if h["name"] == "Subject":
            subject = h["value"]

    body = ""

    if "parts" in payload:
        for part in payload["parts"]:
            if part["mimeType"] == "text/plain":
                data = part["body"].get("data")

                if data:
                    body = base64.urlsafe_b64decode(
                        data
                    ).decode("utf-8")
                    break

    return {
        "id": msg_id,
        "sender": sender,
        "thread_id": msg_data["threadId"],
        "subject": subject,
        "body": body
    }