from langchain_groq import ChatGroq
from .state import Claim, AuditState
from pydantic import BaseModel,Field
from typing import List
from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage
from .tools import web_search

load_dotenv()
#we need this so that the llm finds multiple claims instead of just one
class ExtractionOutput(BaseModel):
    #this collects all the tech claims in the paper
    claims: List[Claim]=Field(description="List of technical dependencies and math formulas")

#binding the llm to the output format we want
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)
def extraction_node(state: AuditState):
    pdf_text=state["pdf_content"]
    system_prompt = (
        "You are a Technical Auditor. Extract every library, hardware, and math formula. "
        "For EACH item found, you MUST call the 'web_search' tool to check its 2026 status."
    )
    
    human_prompt = f"Identify all technical claims in the following text: \n\n {pdf_text}"

    llm_with_tools=llm.bind_tools([web_search])
    #langchain converts llm's json back to python object
    result = llm_with_tools.invoke([
        ("system", system_prompt),
        ("human", f"Audit this text: {pdf_text}")
    ])
    extracted_claims = []
    if result.tool_calls:
        for call in result.tool_calls:
            # We treat each tool call as a 'Claim' object to keep our State happy
            new_claim = Claim(
                text=call["args"].get("query", "Unknown"),
                category="Technical Dependency", # You can refine this logic
                page_label="Extraction Phase"
            )
            extracted_claims.append(new_claim)
    
    #we return a dict that langraph uses to update the 'Audit state'
    return{
        "claims": extracted_claims,
        "messages": [result]
    }

