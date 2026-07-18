from typing import Literal
from langgraph.types import Command, interrupt
from langgraph.graph import END
from ..state import EmailAgentState
from ...services.llm_service import get_llm


def draft_response(state: EmailAgentState) -> Command[Literal["human_review", "__end__"]]:
    """Generate response using context and route based on quality"""

    classification = state.get('classification', {})


    context_sections = []

    if state.get('customer_history'):
        history = state['customer_history']

        # Previous email threads from this sender
        previous_emails = history.get('previous_emails', [])
        if previous_emails:
            threads = []
            for i, email in enumerate(previous_emails, 1):
                ts = f" ({email['timestamp']})" if email.get('timestamp') else ""
                threads.append(
                    f"  [{i}] Subject: {email.get('subject', 'N/A')}{ts}\n"
                    f"      {email.get('snippet', '').strip()}"
                )
            context_sections.append(
                f"Previous emails from this sender ({history.get('email_count', 0)} found):\n"
                + "\n".join(threads)
            )
        else:
            context_sections.append("No previous email history found for this sender.")


    draft_prompt = f"""
        You are a professional customer support representative.

        Write a response to the customer's email.

        Customer Email:
        {state['email_content']}

        Intent: {classification.get('intent', 'unknown')}
        Urgency: {classification.get('urgency', 'medium')}

        Context:
        {chr(10).join(context_sections)}

        Instructions:
        - Return ONLY the email body.
        - Do NOT generate a subject line.
        - Do NOT write "Subject:" anywhere.
        - Do NOT include To/From fields.
        - Do NOT use placeholders like [Your Name].
        - Address the customer's concern directly.
        - Be empathetic and professional.
        - Explain any actions already taken.
        - Use the provided context when relevant.
        - Keep the response concise and practical.

        Formatting Requirements:
        - Start with a greeting (e.g., Dear Rahul Mehta,).
        - Use short paragraphs (2-4 lines maximum).
        - Add a blank line between paragraphs.
        - Use bullet points when asking for information.
        - Avoid large blocks of text.
        - Make the email easy to scan and read.

        Structure:
        1. Acknowledge the issue.
        2. Apologize if appropriate.
        3. Explain the action taken.
        4. Request any additional information if needed.
        5. Explain next steps.
        6. End with:

        Best regards,
        Support Team
        """
    llm = get_llm()
    try:
        response = llm.invoke(draft_prompt)
    except Exception:
        return Command(
            update={
                "draft_response":
                    "We have received your email and will get back to you shortly."
            },
            goto="human_review"
        )

    needs_review = (
        classification.get('urgency') in ['high', 'critical'] or
        classification.get('intent') == 'complex'
    )


    goto = "human_review" if needs_review else END

    return Command(
        update={"draft_response": response.content},  
        goto=goto
    )

def human_review(state: EmailAgentState) -> Command[Literal["__end__"]]:
    """Pause for human review using interrupt and route based on decision"""

    classification = state.get('classification', {})


    human_decision = interrupt({
        "email_id": state.get('email_id',''),
        "original_email": state.get('email_content',''),
        "draft_response": state.get('draft_response',''),
        "urgency": classification.get('urgency'),
        "intent": classification.get('intent'),
        "action": "Please review and approve this response"
    })

    if human_decision.get("approved"):
        edited = human_decision.get("edited_response")
        update_dict = {}
        if edited:
            update_dict["draft_response"] = edited
        return Command(
            update=update_dict,
            goto=END
        )
    else:

        return Command(update={"draft_response": None}, goto=END)

