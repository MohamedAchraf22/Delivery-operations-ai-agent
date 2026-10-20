from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.prebuilt import create_react_agent
from config import GOOGLE_API_KEY
from prompts import get_system_prompt
from tools import export_orders_to_excel, get_order, list_orders


def get_llm(model: str = "gemini-3.1-flash-lite"):
    return ChatGoogleGenerativeAI(
        model=model,
        google_api_key=GOOGLE_API_KEY
    )


def create_agent(llm=None):
    if llm is None:
        llm = get_llm()
    tools = [list_orders, get_order, export_orders_to_excel]
    return create_react_agent(
        model=llm,
        tools=tools,
        prompt=get_system_prompt()
    )

