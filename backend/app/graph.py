import langgraph
from langgraph.graph import StateGraph, START,END
from langchain_groq import ChatGroq
from .nodes import extraction_node, auditor_node, KnowLedgeGrade
from .tools import web_search
from .state import AuditState
from langgraph.prebuilt import ToolNode,tools_condition
from langchain_core.messages import ToolMessage
from typing import Literal
from pydantic import BaseModel,Field
import os
from dotenv import load_dotenv

# Load environment variables from project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(project_root, '.env'))

tools=[web_search]
workflow=StateGraph(AuditState)

llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)
grader_llm=llm.with_structured_output(KnowLedgeGrade)
def route_after_extraction(state: AuditState) -> Literal["web_search", "auditor", "__end__"]:
    #messages = state.get("messages", [])
    # Let's see the types of messages we actually have
    #types = [type(m).__name__ for m in messages]
    #has_searched = any(isinstance(m, ToolMessage) for m in messages)

    # If we found claims and we haven't finished the audit yet
    #if state.get("claims") and not has_searched:
    #    return "web_search"
    #return "__end__"

    print("extraction starting.....")
    messages=state.get("messages",[])
    claims=state.get("claims",[])

    #checking if we've already searched
    has_searched=any(isinstance(m, ToolMessage) for m in messages)
    if has_searched:
        return "auditor"
    if not claims:
        return "__end__"
    
    print(f"ROUTER: Found {len(claims)} claims")
    for i, c in enumerate(claims):
        time_sensitive = getattr(c, 'is_time_sensitive', False)
        print(f"  Claim {i}: '{c.text}' | Time Sensitive: {time_sensitive}")
    
    #extract the ones that are time sensitive
    needs_search = []
    for c in claims:
        if getattr(c, 'is_time_sensitive', False):
            needs_search.append(c)
    print(f"ROUTER: {len(needs_search)} claims need search")
    print(f"ROUTER: Decision - {'web_search' if needs_search else 'auditor'}")
    # TEMP: Force web_search for testing
    if claims:
        return "web_search"
    return "auditor"
    if grade.binary_score == "ambiguous":
        print("Knowledge is STALE. Correcting via Web Search")
        return "web_search"
    
    print("ROUTER: Knowledge is RELIABLE. Skipping Search")
    return "auditor"

workflow.add_node("extractor",extraction_node)
workflow.add_node("web_search",ToolNode(tools))
workflow.add_node("auditor",auditor_node)

workflow.add_edge(START,"extractor")
workflow.add_conditional_edges(
    "extractor",
    route_after_extraction,
    {
        "web_search": "web_search",
        "auditor": "auditor",
        "__end__": END
    }
)
workflow.add_edge("web_search", "auditor")
workflow.add_edge("auditor", END)

chain=workflow.compile()
