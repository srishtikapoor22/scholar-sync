import langgraph
from langgraph.graph import StateGraph, START,END
from .nodes import extraction_node
from .tools import web_search
from .state import AuditState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import ToolMessage

tools=[web_search]
workflow=StateGraph(AuditState)
from typing import Literal

def route_after_extraction(state: AuditState) -> Literal["web_search", "__end__"]:
    messages = state.get("messages", [])
    
    # Let's see the types of messages we actually have
    types = [type(m).__name__ for m in messages]
    print(f"--- ROUTER DEBUG: Message Types are {types} ---")
    
    has_searched = any(isinstance(m, ToolMessage) for m in messages)
    print(f"--- ROUTER DEBUG: Has Searched? {has_searched} ---")
    
    # If we found claims and we haven't finished the audit yet
    if state.get("claims") and not has_searched:
        return "web_search"
    return "__end__"

workflow.add_node("extractor",extraction_node)
workflow.add_node("web_search",ToolNode(tools))

workflow.add_edge(START,"extractor")
workflow.add_conditional_edges(
    "extractor",
    route_after_extraction,
    {
        "web_search": "web_search",
        "__end__": END
    }
)
workflow.add_edge("web_search", END)

chain=workflow.compile()
