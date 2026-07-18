from fastapi import APIRouter, HTTPException, Query

from ..agent.graph import app as langgraph_app
from ..services.email_agent_service import process_latest_email, resume_review, send_email_reply
from ..schemas import ReviewRequest, SendEmailRequest, ProcessEmailRequest
from ..gmail.get_gmail_service import composio_client, get_gmail_auth_config_id

router = APIRouter(tags=["agent"])



@router.get("/auth/connect-gmail")
def connect_gmail(user_id: str = Query(..., description="Your unique user identifier")):
    """
    Generate a Composio OAuth URL so this user can connect their own Gmail.

    Steps:
    1. Call this endpoint with ?user_id=anything-unique
    2. Open the returned `auth_url` in a browser
    3. Complete Google login
    4. Call /auth/status to confirm connection
    """
    try:
        auth_config_id = get_gmail_auth_config_id()
        connection = composio_client.connected_accounts.link(
            user_id=user_id,
            auth_config_id=auth_config_id,
        )
        return {
            "user_id": user_id,
            "auth_url": connection.redirect_url,
            "message": "Open auth_url in your browser to connect Gmail",
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to generate auth URL: {str(e)}"
        )


@router.get("/auth/status")
def auth_status(user_id: str = Query(..., description="Your unique user identifier")):
    """
    Check whether this user has successfully connected their Gmail.
    """
    try:
        accounts = composio_client.connected_accounts.list(
            user_ids=[user_id],
            toolkit_slugs=["gmail"],
            statuses=["ACTIVE"],
        )
        gmail_connected = len(accounts.items) > 0
        return {
            "user_id": user_id,
            "gmail_connected": gmail_connected,
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to check status: {str(e)}"
        )




@router.post("/agent/process-latest")
def process_latest(request: ProcessEmailRequest):
    """Fetch the latest email from this user's Gmail and run it through the agent."""
    result = process_latest_email(user_id=request.user_id)

    if result.get("status") == "no_email":
        return result

    graph_result = result["result"]

    return {
        "thread_id": result["thread_id"],
        "draft_response": graph_result["draft_response"],
        "interrupt": "__interrupt__" in graph_result,
        "sender": graph_result["sender_email"],
        "subject": result["subject"],
    }


@router.post("/agent/review")
def review_email(request: ReviewRequest):
    """Resume a paused human-review interrupt — approve or reject the draft."""
    try:
        result = resume_review(
            thread_id=request.thread_id,
            approved=request.approved,
            edited_response=request.edited_response,
        )
        return {
            "draft_response": result.get("draft_response")
        }
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.post("/agent/send")
def send_email(request: SendEmailRequest):
    """Send the approved draft reply via the user's Gmail."""
    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    state = langgraph_app.get_state(config)

    if not state.values.get("draft_response"):
        raise HTTPException(status_code=400, detail="No draft response found")

    if not state.values.get("subject"):
        raise HTTPException(status_code=400, detail="No subject found")

    if not state.values.get("sender_email"):
        raise HTTPException(status_code=400, detail="No sender found")

    draft   = state.values["draft_response"]
    subject = state.values["subject"]
    sender  = state.values["sender_email"]

    return send_email_reply(
        user_id=request.user_id,
        sender=sender,
        subject=subject,
        body=draft,
        thread_id=request.thread_id,
    )