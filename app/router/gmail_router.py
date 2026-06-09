from fastapi import APIRouter, HTTPException
from ..agent.graph import app
from ..services.email_agent_service import process_latest_email, resume_review, send_email_reply
from ..schemas import ReviewRequest, SendEmailRequest

router = APIRouter(
    prefix="/agent",
    tags=["agent"]
)

@router.post("/process-latest")
def process_latest():

    result = process_latest_email()

    graph_result = result["result"]

    print("RESULT:", result)

    if result.get("status") == "no_email":
        return result

    return {
        "thread_id": result["thread_id"],
        "draft_response": graph_result["draft_response"],
        "interrupt": "__interrupt__" in graph_result,
        "sender": graph_result["sender_email"],
        "subject": result["subject"]
        
    }


@router.post("/review")
def review_email(request: ReviewRequest):
    try:
        result = resume_review(
            thread_id=request.thread_id,
            approved=request.approved,
        )

        return {
            "draft_response": result.get("draft_response")
        }

    except ValueError as e:
        raise HTTPException(
            status_code=400,
            detail=str(e)
        )

@router.post("/send")
def send_email(request: SendEmailRequest):
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    state = app.get_state(config)

    if not state.values.get("draft_response"):
        raise HTTPException(
            status_code=400,
            detail="No draft response found"
        )

    if not state.values.get("subject"):
        raise HTTPException(
            status_code=400,
            detail="No subject found"
        )

    if not state.values.get("sender_email"):
        raise HTTPException(
            status_code=400,
            detail="No sender found"
        )
    
    draft = state.values["draft_response"]
    subject = state.values["subject"]
    sender = state.values["sender_email"]

    return send_email_reply(
        sender=sender,
        subject=subject,
        body=draft,
        thread_id=request.thread_id
    )