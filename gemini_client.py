import os
from google import genai
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")
client = genai.Client(api_key=api_key)

def get_embedding(dic_chunks):
    response = client.models.embed_content(
        model="gemini-embedding-001",
        contents=dic_chunks
    )
    return [response.embeddings[i].values for i in range(len(response.embeddings))]


def ask_gemini(question,content_chunk):
    response = client.models.generate_content(
        model="gemini-3.1-flash-lite",
        contents= f"Answer the question using only the information in the context. If the answer isn't in the context, say I don't know.  Context: {content_chunk}  Question: {question}"
    )
    return response.text
