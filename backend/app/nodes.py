from langchain_groq import ChatGroq
from .state import Claim, AuditState
from pydantic import BaseModel,Field
from typing import List,Literal
from dotenv import load_dotenv
import os
from langchain_core.messages import AIMessage, SystemMessage, ToolMessage

# Load environment variables from project root
project_root = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(project_root, '.env'))
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
    pdf_text = state["pdf_content"]
    print(f"DEBUG: Extracting claims from {len(pdf_text)} characters of PDF content")
    
    system_prompt = (
        """You are a Senior Technical Auditor specializing in Software Engineering and Research.
        Your task is to extract ALL technical claims from the provided text, including:
        - Programming languages and versions
        - Libraries and frameworks
        - Algorithms and models
        - Hardware specifications
        - Software tools and dependencies

        Extract every technical mention, even if it seems basic. Be thorough and comprehensive.

        For each claim, determine if it's time-sensitive (likely to change by 2026):
        - TRUE for specific versions, new technologies, or rapidly evolving tools
        - FALSE for fundamental concepts, established languages, or core algorithms"""
    )

    # Use structured output to extract claims
    try:
        llm_with_structured = llm.with_structured_output(ExtractionOutput)
        structured_result = llm_with_structured.invoke([
            ("system", system_prompt),
            ("human", f"Extract all technical claims from this text:\n\n{pdf_text[:3000]}")  # Limit input size
        ])
        extracted_claims = structured_result.claims if structured_result.claims else []
        print(f"DEBUG: Extracted {len(extracted_claims)} claims via structured output")
        
        # Update time-sensitivity for structured claims if not properly set
        for claim in extracted_claims:
            if not hasattr(claim, 'is_time_sensitive') or claim.is_time_sensitive is None:
                time_sensitive_keywords = [
                    'gpt', 'bert', 'transformers', 'pytorch', 'tensorflow', 'cuda', 
                    'gpu', 'api', 'version', 'latest', 'current', 'deprecated'
                ]
                claim.is_time_sensitive = any(keyword in claim.text.lower() for keyword in time_sensitive_keywords)
    except Exception as e:
        print(f"DEBUG: Structured output failed: {e}, trying simple LLM call...")
        extracted_claims = []
    
    # If no claims found, try a simpler approach
    if not extracted_claims:
        print("DEBUG: No claims from structured output, trying fallback...")
        fallback_prompt = """Extract technical terms, libraries, frameworks, and tools from this text. List them as simple strings, one per line."""
        
        try:
            simple_result = llm.invoke([
                ("system", fallback_prompt),
                ("human", pdf_text[:2000])  # Limit input size
            ])
            
            if hasattr(simple_result, 'content') and simple_result.content:
                # Parse the response into claims
                lines = simple_result.content.strip().split('\n')
                for line in lines:
                    line = line.strip()
                    if line and len(line) > 2:  # Filter out empty/short lines
                        # Remove bullet points, numbers, etc.
                        clean_line = line.lstrip('•-*123456789. ')
                        if clean_line and len(clean_line) < 100:  # Reasonable length limit
                            # Determine if this claim is time-sensitive (needs 2026 status check)
                            time_sensitive_keywords = [
                                'gpt', 'bert', 'transformers', 'pytorch', 'tensorflow', 'cuda', 
                                'gpu', 'api', 'version', 'latest', 'current', 'deprecated'
                            ]
                            is_time_sensitive = any(keyword in clean_line.lower() for keyword in time_sensitive_keywords)
                            
                            extracted_claims.append(Claim(
                                text=clean_line,
                                category="Technical Dependency",
                                page_label="Extraction Phase",
                                is_time_sensitive=is_time_sensitive
                            ))
        except Exception as e:
            print(f"DEBUG: Simple LLM call also failed: {e}")
    
    print(f"DEBUG: Final extracted claims: {[c.text for c in extracted_claims[:5]]}")  # Show first 5
    
    print(f"DEBUG: Final extracted claims: {[c.text for c in extracted_claims]}")
    
    # Return the claims
    return {
        "claims": extracted_claims,
        "messages": [AIMessage(content=f"Extracted {len(extracted_claims)} claims from PDF")]
    }

def auditor_node(state:AuditState):
    search_results=[m.content for m in state["messages"] if isinstance(m, ToolMessage)]
    search_results_text="\n\n".join(search_results)

    system_prompt=(
        """You are a Senior AI Research Auditor. Your task is to compare a 2021 technical paper 
    against 2026 real-world data and provide a final audit report.

    PAPER CONTENT:
    {content}

    2026 SEARCH DATA:
    {search_results}

    Provide a professional Audit Report with these EXACT sections:

## Executive Summary
(One sentence on the current relevance of the paper)

## Verified Foundations
(List things that are still true/standard in 2026)

## Status Alerts (2026)
(List models/libraries that are deprecated, updated, or replaced. 
Be specific: mention PyTorch 2.11 or GPT-4/5 if found in search.)

## Critical Discrepancies
(Correct any specific "stale" facts from the paper using the search data)
        """
    )
    human_content = f"ORIGINAL PAPER CONTENT: {state['pdf_content']}\n\n2026 SEARCH RESULTS: {search_results_text}"
    report=llm.invoke([
        SystemMessage(content=system_prompt),
        ("human",human_content)
    ])

    # Extract just the final formatted report from the response
    content = report.content
    if "The final answer is:" in content:
        # Extract everything after "The final answer is:"
        final_answer = content.split("The final answer is:", 1)[1].strip()
        # Remove any markdown code blocks if present
        if final_answer.startswith("```") and "```" in final_answer:
            final_answer = final_answer.split("```", 2)[1]
        content = final_answer

    return{
        "messages":[AIMessage(content=content)]
    }


