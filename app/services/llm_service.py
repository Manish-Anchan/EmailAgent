from langchain_groq import ChatGroq
from ..config import settings


def get_llm():
    llm = ChatGroq(model=settings.model_name, api_key=settings.groq_api_key)
    return llm
