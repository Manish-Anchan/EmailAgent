from ..state import EmailAgentState
from typing import Literal

from langgraph.types import Command
import uuid



def bug_tracking(state: EmailAgentState) -> Command[Literal["draft_response"]]:
    """Create or update bug tracking ticket"""


    ticket_id = f"BUG-{str(uuid.uuid4())[:8]}" 
    return Command(
        update={
            "search_results": [f"Bug ticket {ticket_id} created"],
            "current_step": "bug_tracked"
        },
        goto="draft_response"
    )