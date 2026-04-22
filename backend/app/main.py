from dotenv import load_dotenv
from .graph import chain
import os
from .pdf_utils import extract_text,chunk_text

load_dotenv()


def run_audit(pdf_path):
    #extract blocks
    records=extract_text(pdf_path)
    chunks = chunk_text(records)
    valid_contents = [c.strip() for c in chunks if isinstance(c, str) and c.strip()]
    if not valid_contents and chunks and isinstance(chunks[0], dict):
        valid_contents = [c.get('content', '').strip() for c in chunks if c.get('content')]

    # Join the first 15 chunks
    selected_content = "\n\n".join(valid_contents[:15])
    
    print(f"DEBUG: Chunks type: {type(chunks[0]) if chunks else 'None'}")
    print(f"DEBUG: Characters being sent: {len(selected_content)}")

    if len(selected_content) < 50:
        print("WARNING: selected_content is still very short.")

    initial_state={
        "pdf_content":selected_content,
        "claims":[],
        "messages": [],
        "search_performed": False
    }
    print("Running scholar-sync check....")

    last_output=None
    last_node=None
    for chunk in chain.stream(initial_state,stream_mode="updates"):
        for node_name, output in chunk.items():
            last_node=node_name
            last_output=output
            print(f"node executing:{node_name}")
            
            if "claims" in output:
                for i, claim in enumerate(output["claims"]):
                    print(f"  [{i+1}] Found: {claim.text} ({claim.category})")
            if "messages" in output:
                for msg in output["messages"]:
                    if hasattr(msg, "content") and node_name == "web_search":
                        print(f"SEARCH RESULT: {str(msg.content)[:200]}...")

    if node_name == "auditor" and "messages" in last_output:
        print("\n--- FINAL AUDIT REPORT ---")
        print(last_output["messages"][-1].content)

if __name__=="__main__":
    run_audit(r"C:\Users\Srishti\scholar-sync\scholar-sync\testdoc.pdf")