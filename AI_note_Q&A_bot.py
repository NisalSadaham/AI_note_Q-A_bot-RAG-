import gemini_client as gc
import numpy as np
from pypdf import PdfReader
import os
import json
import vector_store as vs


def pdf_opener(file_name):
    try:
        reader = PdfReader(file_name)
        text = ""
        for page in reader.pages:
            page_text = page.extract_text()
            page_text = page_text.replace("\n", " ")
            text += page_text + "\n\n"
    except FileNotFoundError:
        print("File not found.")
        return None
    return text

def note_opener(file_name):
    try:
        with open(file_name, 'r') as file:
            text = file.read()
    except FileNotFoundError:
        print("File not found.")
        return None
    return text

def get_chunks(text):
    if text is None:
        print("No text to chunk.")
        return None
    chunks = text.split("\n\n")
    filterd_chunks = [chunk for chunk in chunks if chunk.strip() != ""]
    return filterd_chunks

def build_chunk_dicts(text):
    chunks = get_chunks(text)
    if chunks is None:
        return None
    else:
        dic_chunks = [{"Index": index , "chunk":chunk}for index,chunk in enumerate(chunks)]
        return dic_chunks  

def query_collection(question, n_results=1):
    question_embedding = gc.get_embedding([question])[0]
    results = vs.collection.query(
        query_embeddings=[question_embedding],
        n_results=n_results
    )
    top_chunk = results['documents'][0][0]
    return top_chunk
    
def menu():
    print("Welcome to the Note Q&A Bot!")
    print("1. Ask a question")
    print("2. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    return choice

def file_extension_extractor(file_name):
    extension = os.path.splitext(file_name)[1]
    return extension

def file_opener(file_name):
    extension = file_extension_extractor(file_name)
    match extension:
        case ".txt":
            text = note_opener(file_name)
        case ".pdf":
            text = pdf_opener(file_name)
        case _:
            print("Unsupported file type.")
            return None
    return text

def save_file_name(file_name):
    with open("file_name.json", 'w') as f:
        json.dump(file_name, f)

def load_file_name():
    try:
        with open("file_name.json", 'r') as f:
            file_name = json.load(f)
    except FileNotFoundError:
        return None
    return file_name

def new_chunks_creator():
        file_name = input("Enter the name of the note file: ")
        save_file_name(file_name)
        text = file_opener(file_name)
        dic_chunks = build_chunk_dicts(text)
        only_chunk = [chunk["chunk"] for chunk in dic_chunks]
        embeddings = gc.get_embedding(only_chunk)
        new_dic_chunks = [{"Index":dic_chunks[i]["Index"], "chunk": dic_chunks[i]["chunk"], "embedding": embeddings[i]} for i in range(len(dic_chunks))]
        vs.add_chunks_to_collection(new_dic_chunks)

def main():
    
    file_name = load_file_name()
    if  vs.collection.count() == 0 or file_name is None:
         new_chunks_creator()
    else:
        choice = input(f"Found existing  data for file '{file_name}'. Do you want to use it? (y/n): ")
        if choice.lower() == "y":
            pass
        elif choice.lower() == "n":
            new_chunks_creator()
        else:
            print("Invalid choice. Exiting the program.")
            return
    while True:
        choice = menu()
        if choice == 1:
            question = input("Enter your question: ")
            relevant_chunk = query_collection(question)
            answer = gc.ask_gemini(question, relevant_chunk)
            print("Answer:", answer)
        elif choice == 2:
            print("Exiting the program.")
            break
        elif choice is None:
            continue
        else:
            print("Invalid choice. Please try again.")
            continue
if __name__ == "__main__":
    main()

