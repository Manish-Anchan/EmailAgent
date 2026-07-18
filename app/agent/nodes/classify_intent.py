from typing import Literal
from langgraph.types import Command
from langchain_core.messages import HumanMessage
from ..state import EmailAgentState, EmailClassification
from ...services.llm_service import get_llm



def classify_intent(state: EmailAgentState) -> Command[Literal["fetch_email_history", "bug_tracking"]]:
    """Use LLM to classify email intent and urgency, then route accordingly"""
    
    llm = get_llm()
    structured_llm = llm.with_structured_output(EmailClassification)

    classification_prompt = f"""
    Analyze this customer email and classify it:

    Email: {state['email_content']}
    From: {state['sender_email']}

    Provide classification including intent, urgency, topic, and summary.
    """
    try:
        classification = structured_llm.invoke(
            classification_prompt
        )
    except Exception:
        classification = {
            "intent": "complex",
            "urgency": "high",
            "topic": "unknown",
            "summary": "Classification failed"
        }


    if classification['intent'] == 'bug':
        goto = "bug_tracking"
    else:
        goto = "fetch_email_history"

    return Command(
        update={"classification": classification},
        goto=goto
    )