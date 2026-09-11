# Chat with your PDF

This mini-project uses retrieval-augmented generation (RAG) to answer questions from an uploaded PDF and cite the pages used.

## Setup

From the repository root, create and activate a virtual environment, then install the dependencies:

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r Class34/requirements.txt
```

Set your Gemini API key in a `.env` file in the repository root:

```text
GEMINI_API_KEY=your-key-here
```

Replace `your-key-here` with your real key and restart the app after creating or changing the file.

## Run

```bash
python Class34/pdf_chat.py
```

Upload a PDF in the browser, wait for the indexing message, and then ask questions about the document.

The index is held in memory and is rebuilt whenever a new PDF is uploaded. The first indexing run also downloads the `all-MiniLM-L6-v2` embedding model.