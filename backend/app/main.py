from dotenv import load_dotenv
from .graph import chain
import os

load_dotenv()

def run_audit():
    mock_pdf_text="""
    Our implementation uses PyTorch 1.13 and the bitsandbytes v0.41 library 
    for 4-bit quantization. We tested this on a single NVIDIA A100 GPU 
    using the Adam optimizer with a learning rate of 2e-4.
    """
    initial_state={
        "pdf_content":mock_pdf_text,
        "claims":[],
        "messages": [],
        "search_performed": False
    }
    print("Running scholar-sync check....")

    for chunk in chain.stream(initial_state,stream_mode="updates"):
        for node_name, output in chunk.items():
            print(f"node executing:{node_name}")
            
            if "claims" in output:
                for i, claim in enumerate(output["claims"]):
                    print(f"  [{i+1}] Found: {claim.text} ({claim.category})")
            if "messages" in output:
                for msg in output["messages"]:
                    if hasattr(msg, "content") and node_name == "web_search":
                        print(f"🔍 SEARCH RESULT: {msg.content[:200]}...")

if __name__=="__main__":
    run_audit()