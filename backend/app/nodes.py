from langchain_groq import ChatGroq
from .state import Claim, AuditState
from pydantic import BaseModel,Field
from typing import List,Literal
from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage
from .tools import web_search
from langchain_core.messages import ToolMessage, SystemMessage

load_dotenv()
#we need this so that the llm finds multiple claims instead of just one
class ExtractionOutput(BaseModel):
    #this collects all the tech claims in the paper
    claims: List[Claim]=Field(description="List of technical dependencies and math formulas")


class KnowLedgeGrade(BaseModel):
    """Binary score for the reliability of extracted technical claims."""
    binary_score:Literal["reliable","ambiguous"]=Field(
        description="Score 'reliable' if the claims are common knowledge; 'ambiguous' if they require a 2026 status check."
    )
#binding the llm to the output format we want
llm = ChatGroq(
    temperature=0, 
    model_name="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

def extraction_node(state: AuditState):
    pdf_text=state["pdf_content"]
    system_prompt = (
        """You are a Senior Technical Auditor specializing in Software Engineering and Research.
        Your task is to extract technical claims (libraries, frameworks, hardware, and algorithms).

        CRITICAL: When generating a search query for a claim:
        1. Append the domain context (e.g., instead of 'Adam', use 'Adam optimizer machine learning').
        2. Instead of 'GPT-3', use 'GPT-3 model status and replacements 2026'.
        3. Instead of 'PyTorch', use 'PyTorch latest version and features 2026'.
        ### CATEGORIZATION RULES:
        1. is_time_sensitive = FALSE (Foundational): 
        - Core Math/Statistics (e.g., Euclidean Geometry, Bayesian Inference).
        - Foundational CS Concepts (e.g., Linked Lists, BFS, Transformers, RNNs).
        - Established Languages (e.g., Python, C++, Java).

        2. is_time_sensitive = TRUE (Volatile):
        - Specific Versions (e.g., React 19, CUDA 12.1).
        - Brand New Research/Models (e.g., GPT-5, Llama-4, specific 2026 hardware).
        - Cloud Services/API Endpoints (e.g., AWS Bedrock, Anthropic API).

        ### FORMATTING RULE:
        - The 'query' field must be the PURE name of the concept. 
        - DO NOT append "2026 status" or "updates" to the query.
        - Use the 'is_time_sensitive' boolean to indicate if a search is actually necessary."""
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
                page_label="Extraction Phase",
                is_time_sensitive=call["args"].get("is_time_sensitive", True)
            )
            extracted_claims.append(new_claim)
    
    #we return a dict that langraph uses to update the 'Audit state'
    return{
        "claims": extracted_claims,
        "messages": [result]
    }

def auditor_node(state:AuditState):
    search_results=[m.content for m in state["messages"] if isinstance(m, ToolMessage)]
    search_results_text="\n\n".join(search_results)

    system_prompt=(
        """You are a Senior AI Research Auditor. Your task is to compare a 2021 technical paper 
    against 2026 real-world data.

    PAPER CONTENT:
    {content}

    2026 SEARCH DATA:
    {search_results}

    Provide a professional Audit Report with these EXACT sections:
    ##Executive Summary
    (One sentence on the current relevance of the paper)

    ##Verified Foundations
    (List things that are still true/standard in 2026)

    ##Status Alerts (2026)
    (List models/libraries that are deprecated, updated, or replaced. 
    Be specific: mention PyTorch 2.11 or GPT-4/5 if found in search.)

    ##Critical Discrepancies
    (Correct any specific "stale" facts from the paper using the search data)
        """
    )
    human_content = f"ORIGINAL PAPER CONTENT: {state['pdf_content']}\n\n2026 SEARCH RESULTS: {search_results_text}"
    report=llm.invoke([
        SystemMessage(content=system_prompt),
        ("human",human_content)
    ])

    return{
        "messages":[AIMessage(content=report.content)]
    }


