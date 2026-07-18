from ..state import EmailAgentState
from typing import Literal

from langgraph.types import Command
import uuid



def bug_tracking(state: EmailAgentState):
    """Create or update bug tracking ticket"""


    ticket_id = f"BUG-{str(uuid.uuid4())[:8]}" 
    return {
        "search_results": [f"Bug ticket {ticket_id} created"],
    }