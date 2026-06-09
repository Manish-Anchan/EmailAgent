from pydantic import BaseModel


class ReviewRequest(BaseModel):
    thread_id: str
    approved: bool


class SendEmailRequest(BaseModel):
    thread_id: str