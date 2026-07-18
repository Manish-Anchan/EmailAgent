from sqlalchemy import Column, String, Text, TIMESTAMP, CheckConstraint, Index
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.sql import text
import uuid

from app.database import Base


class EmailHistory(Base):
    __tablename__ = "email_history"

    id = Column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    email_id = Column(String(255), unique=True)
    thread_id = Column(String(255))

    sender_email = Column(String(255), nullable=False)
    recipient = Column(String(255))

    subject = Column(Text)
    content = Column(Text)
    draft_response = Column(Text)

    direction = Column(String(10), nullable=False)

    timestamp = Column(
        TIMESTAMP(timezone=True),
        nullable=False,
        server_default=text("now()")
    )

    __table_args__ = (
        CheckConstraint(
            "direction IN ('inbound', 'outbound')",
            name="direction_check"
        ),
        Index(
            "idx_email_history_sender",
            "sender_email",
            timestamp.desc()
        ),
    )