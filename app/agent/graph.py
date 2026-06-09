from langgraph.checkpoint.memory import MemorySaver
from langgraph.types import RetryPolicy
from langgraph.graph import StateGraph, START, END

from .state import EmailAgentState
from .nodes import response_nodes, classify_intent, search_and_track
from .nodes.email_history import make_fetch_email_history

memory = MemorySaver()


def create_graph(db=None):
    workflow = StateGraph(EmailAgentState)

    workflow.add_node("classify_intent", classify_intent.classify_intent)
    workflow.add_node("bug_tracking", search_and_track.bug_tracking)

    workflow.add_node(
        "fetch_email_history",
        make_fetch_email_history(db),
    )

    workflow.add_node("draft_response", response_nodes.draft_response)
    workflow.add_node("human_review", response_nodes.human_review)

    workflow.add_edge(START, "classify_intent")
    workflow.add_edge("bug_tracking", "fetch_email_history")
    workflow.add_edge("human_review", END)

    return workflow.compile(checkpointer=memory)


app = create_graph()