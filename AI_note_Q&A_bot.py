import gemini_client as gc
import numpy as np



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
        return
    chunks = text.split("\n\n")
    return chunks

def build_chunk_dicts(text):
    chunks = get_chunks(text)
    if chunks is None:
        return
    else:
        dic_chunks = [{"Index": index , "chunk":chunk}for index,chunk in enumerate(chunks)]
        return dic_chunks  

def find_most_relevant(question, dic_chunks):
    question_embedding = gc.get_embedding([question])[0]
    best_score_so_far = -1
    best_chunk_so_far = None

    for chunk in dic_chunks:
        chunk_embedding = chunk["embedding"]
        similarity = np.dot(question_embedding,chunk_embedding)/(np.linalg.norm(question_embedding)*np.linalg.norm(chunk_embedding))

        if best_score_so_far < similarity:
            best_score_so_far = similarity
            best_chunk_so_far = chunk["chunk"]
    return best_chunk_so_far

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

def main():
    file_name = input("Enter the name of the note file: ")
    text = note_opener(file_name)
    dic_chunks = build_chunk_dicts(text)
    only_chunk = [chunk["chunk"] for chunk in dic_chunks]
    embeddings = gc.get_embedding(only_chunk)
    new_dic_chunks = [{"Index":dic_chunks[i]["Index"], "chunk": dic_chunks[i]["chunk"], "embedding": embeddings[i]} for i in range(len(dic_chunks))]
    while True:
        choice = menu()
        if choice == 1:
            question = input("Enter your question: ")
            relevant_chunk = find_most_relevant(question, new_dic_chunks)
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

