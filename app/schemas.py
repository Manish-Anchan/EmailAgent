from pydantic import BaseModel


class ReviewRequest(BaseModel):
    thread_id: str
    approved: bool
    edited_response: str | None = None


class ProcessEmailRequest(BaseModel):
    user_id: str   # Composio user_id — identifies which Gmail account to use


class SendEmailRequest(BaseModel):
    thread_id: str
    user_id: str   # Needed to send via the correct user's Gmail