import pymupdf as fitz
import re
from langchain_text_splitters import RecursiveCharacterTextSplitter
import os

def extract_text(file_path):
    import os
    import fitz

    if not os.path.exists(file_path):
        print(f"❌ ERROR: File not found at {os.path.abspath(file_path)}")
        return []

    doc_objects = []
    try:
        doc = fitz.open(file_path)
        page_count = len(doc)
        print(f"DEBUG: PDF opened successfully. Total pages: {page_count}")

        if page_count == 0:
            print("⚠️ WARNING: PDF has 0 pages.")
            return []

        for page_num in range(page_count):
            page = doc.load_page(page_num)
            # Use 'blocks' but with a safety check
            blocks = page.get_text("blocks")
            
            for b in blocks:
                # b is a tuple. The text is always at index 4.
                if len(b) > 4:
                    text = str(b[4]).strip()
                    if text:
                        doc_objects.append({
                            "content": text,
                            "page_num": page_num + 1,
                            "source": file_path
                        })
        doc.close()

    except Exception as e:
        print(f"❌ EXTRACTION CRASHED: {e}")
        return []

    print(f"DEBUG: Total blocks captured: {len(doc_objects)}")
    return doc_objects


def chunk_text(doc_objects, chunk_size=2000, chunk_overlap=200):
    full_text="\n\n".join([obj["content"] for obj in doc_objects])
    splitter=RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    chunks=splitter.split_text(full_text)
    return chunks

if __name__ == "__main__":
    # You can test this by running: python -m backend.app.pdf_utils
    # Replace with a path to a PDF on your machine
    sample_path = "test_document.pdf" 
    print("--- Testing PDF Extraction ---")
    result = extract_text(sample_path)
    print(result[:1000]) # Print first 1000 characters