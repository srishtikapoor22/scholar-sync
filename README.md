# Scholar Sync

Scholar Sync is a research paper audit tool that extracts content from uploaded documents, performs Tavily web search lookups, identifies claims and outdated dependencies, and streams a technical audit report through a web UI. It uses 3 main workflow nodes (`extractor`, `web_search`, `auditor`) to drive the audit pipeline.

The audit workflow follows this pipeline:

- `START -> extractor`
- `extractor` conditionally routes to `web_search` or `auditor`
- `web_search -> auditor`
- `auditor -> END`

## Project Structure

- `backend/` - FastAPI-based audit backend and PDF extraction utilities
- `frontend/` - Next.js app for PDF upload, preview, and live audit streaming
- `requirements.txt` - Python dependencies for backend services
- `frontend/package.json` - frontend dependencies and scripts
- `testdoc.pdf` - sample PDF used by the backend when no file is provided

## Key Features

- Upload and preview PDF documents in the browser
- Extract PDF text using `pymupdf` and split into chunks
- Stream audit events via Server-Sent Events (SSE)
- Detect claims and deprecated/outdated dependencies from PDF content
- Perform live Tavily-powered search reference lookups
- Render audit findings, search references, and a generated audit report

## Requirements

### Backend

- Python 3.11+ (recommended)
- `pymupdf`
- `langgraph`
- `langchain`
- `langchain-groq`
- `langchain-community`
- `langchain-text-splitters`
- `langchain-tavily`
- `tavily-python`
- `pydantic`
- `python-dotenv`
- `docling`
- `pypdf`
- `mermaid-python`
- `fastapi`
- `uvicorn`

Install backend dependencies with:

```bash
pip install -r requirements.txt
```

### Frontend

- Node.js 20+ (recommended)
- npm

Install frontend dependencies from the `frontend` folder:

```bash
cd frontend
npm install
```

## Running the App

### Start the backend

From the repository root:

```bash
uvicorn backend.app.server:app --reload --host 0.0.0.0 --port 8000
```

### Start the frontend

From the repository root:

```bash
cd frontend
npm run dev
```

The frontend runs at `http://localhost:3000` and proxies audit requests to the backend.

## Usage

1. Open the Next.js app in your browser.
2. Upload a PDF file using the UI.
3. Click **Start audit**.
4. Watch audit events stream in the dashboard:
   - extracted claims
   - deprecated dependencies
   - search references
   - generated audit report

## API Routes

- `POST /api/upload` - saves the uploaded PDF to `frontend/public/uploaded.pdf`
- `GET /api/audit` - proxies SSE audit requests to the backend at `http://localhost:8000/audit`
- `GET /audit` (backend) - streams audit events from the FastAPI server

## Notes

- The backend uses `backend/app/pdf_utils.py` to extract text from PDFs and chunk it for processing.
- The SSE implementation is in `backend/app/server.py` and publishes `claim`, `deprecated`, `search`, `report`, and `status` events.
- The frontend preview is handled by `frontend/components/simple-pdf-viewer.tsx`.
