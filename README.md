# Notes Q&A Bot — Simple RAG System

A simple **Retrieval-Augmented Generation (RAG)** system built with Python that allows users to ask questions about the contents of a text-based note file.

The project combines **text chunking, embeddings, cosine similarity, and Gemini** to retrieve the most relevant section of a document before generating an answer.

## How It Works

The system follows a basic RAG pipeline:

```text
Note File
   ↓
Read Text
   ↓
Split Into Chunks
   ↓
Generate Embeddings
   ↓
Store Chunks + Embeddings
   ↓
User Question
   ↓
Generate Question Embedding
   ↓
Calculate Similarity
   ↓
Retrieve Most Relevant Chunk
   ↓
Send Question + Context to Gemini
   ↓
Generate Answer
```

## Features

- Read questions from a local text file
- Split notes into separate chunks
- Generate embeddings for each chunk
- Generate an embedding for the user's question
- Compare embeddings using cosine similarity
- Retrieve the most relevant chunk
- Use Gemini to generate an answer using the retrieved context
- Simple command-line interface

## Technologies Used

- **Python**
- **Gemini API** — Embeddings and answer generation
- **NumPy** — Vector calculations and cosine similarity
- **File I/O** — Reading local notes

## Project Structure

```text
Notes Q&A Bot/
│
├── AI_note_Q&A_bot.py
├── gemini_client.py
├── notes.txt
├── .env
├── .gitignore
└── README.md
```

## Installation

### 1. Clone the repository

```bash
git clone <your-repository-url>
cd "Notes Q&A Bot"
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it on macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install numpy google-genai python-dotenv
```

### 4. Configure the Gemini API key

Create a `.env` file:

```env
GEMINI_API_KEY=your_api_key_here
```

Make sure `.env` is included in `.gitignore` so the API key is never pushed to GitHub.

## Usage

Run the program:

```bash
python AI_note_Q&A_bot.py
```

The program will ask for the name of the note file:

```text
Welcome to the Note Q&A Bot!
Enter the name of the note file:
```

After loading the notes, you can ask questions about their contents.

Example:

```text
1. Ask a question
2. Exit

Enter your choice: 1
Enter your question: What is inheritance?
```

The system retrieves the note chunk that is most semantically similar to the question and sends that context to Gemini to generate the answer.

## RAG Components

### 1. Document Loading

The program reads a local text file and stores its contents as a string.

```python
with open(file_name, 'r') as file:
    text = file.read()
```

### 2. Chunking

The document is divided into chunks using blank lines as separators.

```python
chunks = text.split("\n\n")
```

Each chunk is assigned an index.

### 3. Embeddings

Embeddings are generated for each chunk using the Gemini embedding model.

The resulting vectors represent the semantic meaning of the text numerically.

### 4. Similarity Search

When the user asks a question, an embedding is generated for the question.

The system then compares the question embedding with every document chunk using cosine similarity:

```text
similarity =
(question · chunk) /
(||question|| × ||chunk||)
```

The chunk with the highest similarity score is selected as the relevant context.

### 5. Answer Generation

The selected chunk and the user's question are passed to Gemini.

Gemini then generates an answer based on the retrieved context.

## Example

Suppose the notes contain:

```text
Inheritance allows a class to acquire properties and methods
from another class.

Encapsulation is the process of bundling data and methods
together while controlling access to the data.
```

The user asks:

```text
What is inheritance?
```

The system:

1. Creates an embedding for the question.
2. Compares it against the embeddings of the note chunks.
3. Finds the inheritance-related chunk.
4. Sends the question and retrieved chunk to Gemini.
5. Generates the final answer.

## What I Learned

This project was built to understand the fundamentals of **Retrieval-Augmented Generation** rather than relying entirely on an LLM's existing knowledge.

Through this project, I practiced:

- Working with AI APIs
- Generating and using embeddings
- Representing text as vectors
- Vector similarity calculations
- Cosine similarity
- Basic information retrieval
- Connecting retrieval systems with LLMs
- Structuring Python projects into separate modules
- Working with environment variables and API keys

## Limitations

This is a learning-focused implementation of RAG and has several limitations:

- Uses simple paragraph-based chunking
- Searches every chunk sequentially
- Does not use a vector database
- Only retrieves the single highest-scoring chunk
- Does not implement persistent embedding storage
- No advanced document preprocessing
- Currently designed for text files
- No conversation history
- No evaluation system for retrieval quality

These limitations are intentional because the project focuses on understanding the core concepts behind a RAG pipeline.

## Possible Future Improvements

Some possible improvements include:

- Better chunking strategies
- Configurable chunk size and overlap
- Top-K retrieval instead of retrieving only one chunk
- Add a vector database such as FAISS or Chroma
- Store embeddings so they do not need to be regenerated
- Support PDF and other document formats
- Add conversation history
- Improve prompt construction
- Add retrieval evaluation
- Build a web interface
- Add source citations to generated answers

## Project Goal

The goal of this project was to build a small RAG system from the ground up and understand what happens between a user's question and the final LLM-generated response.

It serves as a foundation for building more advanced AI applications involving **embeddings, retrieval systems, APIs, and LLMs**.
