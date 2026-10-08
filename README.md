# Notes Q&A Bot

A small retrieval-augmented generation (RAG) app. Upload your own notes (`.txt` or `.pdf`), pick a file, ask a question, and get an answer grounded in that file's content.

Built as a learning project: the chunking, embedding, vector search, API and frontend are all written by hand, without a RAG framework.

## How it works

1. **Upload.** A note file is read, split into sentences, and grouped into chunks.
2. **Embed.** Each chunk is turned into an embedding with the Gemini API.
3. **Store.** Chunks, embeddings and metadata (`filename`, `subject`) are saved in a local ChromaDB collection. The uploaded file itself is deleted afterwards, since only the chunks are needed to answer questions.
4. **Ask.** The question is embedded, ChromaDB returns the closest chunks from the selected file (filtered by metadata), and Gemini answers using only those chunks.

## Project structure

| File | Purpose |
| --- | --- |
| `api.py` | FastAPI app: `GET /files`, `POST /ask`, `POST /upload` |
| `AI_note_QA_bot.py` | Core pipeline (file reading, chunking, `new_chunks_creator`) and the original terminal menu |
| `vector_store.py` | ChromaDB collection, `add_chunks_to_collection` |
| `gemini_client.py` | Embeddings and answer generation with Gemini |
| `frontend/index.html`, `frontend/script.js` | Browser interface |
| `known_files.json` | List of uploaded files and their subjects (created at runtime) |
| `chroma_db/` | Vector database (created at runtime) |

## Setup

Developed and tested on Python 3.12.3.

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Create a `.env` file in the project folder with your Gemini API key (get one from Google AI Studio):

```
GEMINI_API_KEY=your_key_here
```

## Run

Start the API from the project folder (the data paths are relative to it):

```bash
fastapi dev api.py
```

Then open `frontend/index.html` with a local server such as the VS Code Live Server extension. The interactive API docs are at `http://127.0.0.1:8000/docs`.

The original terminal version still works:

```bash
python3 AI_note_QA_bot.py
```

## Supported input and limits

- File types: `.txt` and `.pdf` (text-based PDFs; scanned PDFs without a text layer are rejected as empty).
- Uploads are limited in size (see `MAX_UPLOAD_BYTES` in `api.py`).
- Duplicate filenames are rejected.
- The free Gemini tier has rate limits, so very large files or many requests can return a 429 or 503 error. The interface shows a friendly message when that happens.

## Known limitations and ideas for next steps

- **No evaluation yet.** The next step is a small question set with known answers to measure retrieval quality while tuning chunk size and the number of retrieved chunks.
- **One chunk by default in the terminal flow**, three in the web route. Overlapping chunks and reranking are untested.
- **No conversation memory.** Each question is answered independently.
- **Shared data.** All users see the same file list and collection, so it is only suitable for a single person or a small trusted group.
- **No login or HTTPS.** Fine for local use; it needs authentication before being exposed to the internet.
- **PDF text extraction** keeps extra whitespace from the source file.
