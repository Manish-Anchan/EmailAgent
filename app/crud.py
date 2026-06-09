from sqlalchemy.orm import Session
from .models import EmailHistory

def create_email_history(db: Session, email_data: dict):
    db_email = EmailHistory(
        email_id=email_data.get("id"),
        thread_id=email_data.get("thread_id"),
        sender_email=email_data.get("sender"),
        recipient=email_data.get("recipient"),
        subject=email_data.get("subject"),
        content=email_data.get("body"),
        direction="inbound"  
    )
    db.add(db_email)
    db.commit()
    db.refresh(db_email)
    return db_email
