from sqlalchemy.orm import Session
from .models import EmailHistory

def create_email_history(db: Session, email_data: dict):
    existing = db.query(EmailHistory).filter(EmailHistory.email_id == email_data.get("id")).first()
    if existing:
        if not existing.content and email_data.get("body"):
            existing.content = email_data.get("body")
            db.commit()
            db.refresh(existing)
        return existing
        
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

def update_email_draft(db: Session, email_id: str, draft: str):
    db_email = db.query(EmailHistory).filter(EmailHistory.email_id == email_id).first()
    if db_email:
        db_email.draft_response = draft
        db.commit()
        db.refresh(db_email)
    return db_email
