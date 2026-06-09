
from ..gmail import extract_email, get_mail, send_mail
from ..agent.graph import create_graph
from ..database import get_db
from .. import crud
from langgraph.types import Command



def process_latest_email():
    try:
        email = get_mail.get_latest_email()
    except Exception as e:
        raise ValueError(f"Failed to fetch email: {str(e)}")

    if not email:
        return {"status": "no_email"}

    print("\nEMAIL RECEIVED\n")
    print("FROM:", email["sender"])
    print("SUBJECT:", email["subject"])
    
    db = next(get_db())
    try:
        try:
            crud.create_email_history(db, email)
            print("Email saved to history.")
        except Exception as e:
            print(f"Warning: Failed to save email to history: {e}")

        initial_state = {
            "email_content": email["body"],
            "sender_email": email["sender"],
            "subject": email["subject"],
            "email_id": email["id"]
        }

        config = {
            "configurable": {
                "thread_id": email["thread_id"]
            }
        }


        executor = create_graph(db=db)
        
        result = executor.invoke(
            initial_state,
            config=config
        )

        return {
            "thread_id": email["thread_id"],
            "subject": email["subject"],
            "result": result
        }
    finally:
        db.close()


def resume_review(
    thread_id: str,
    approved: bool,
):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }
    
    db = next(get_db())
    try:
        executor = create_graph(db=db)
        
        state = executor.get_state(config)
        print(state)

        if not state.interrupts:
            raise ValueError("No pending review for this thread")

        result = executor.invoke(
            Command(
                resume={
                    "approved": approved,
                }
            ),
            config=config
        )

        return result
    finally:
        db.close()



def send_email_reply(
    sender,
    subject,
    body,
    thread_id
):

    try:
        send_mail.send_reply(
            email=extract_email.extract_email(sender),
            subject=subject,
            body=body,
            thread_id=thread_id
        )
    except Exception as e:
        return {
            "status": "failed",
            "error": str(e)
        }

    return {
        "status": "sent"
    }

