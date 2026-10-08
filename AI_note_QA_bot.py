import gemini_client as gc
from pypdf import PdfReader
import os
import json
import vector_store as vs

class FileAlreadyExistsError(Exception):
    pass
class EmptyTextError(Exception):
    pass
class UnSupportedFileType(Exception):
    pass

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

def query_collection(question, n_results=3,filename=None):
    question_embedding = gc.get_embedding([question])[0]
    results = vs.collection.query(
        query_embeddings=[question_embedding],
        where={"filename":filename} if filename else None,
        n_results=n_results

    )
    chunk = results['documents'][0]
    separator = "\n'----'\n"
    return separator.join(chunk)

    
    
def menu():
    print("Welcome to the Note Q&A Bot!")
    print("1. Ask a question")
    print("2. Add a new file to the collection")
    print("3. Exit")
    try:
        choice = int(input("Enter your choice: "))
    except ValueError:
        print("Invalid input. Please enter a number.")
        return None
    return choice

def file_extension_extractor(file_name):
    extension = os.path.splitext(file_name)[1]
    return extension.lower()

def file_opener(file_name):
    extension = file_extension_extractor(file_name)
    match extension:
        case ".txt":
            text = note_opener(file_name)
        case ".pdf":
            text = pdf_opener(file_name)
        case _:
            raise UnSupportedFileType("This file type is not supported")
    return text

def save_known_files(known_file_names):
    with open("known_files.json", 'w') as f:
        json.dump(known_file_names, f)

def load_known_files():
    try:
        with open("known_files.json", 'r') as f:
            known_file_names = json.load(f)
    except FileNotFoundError:
        return []
    return known_file_names

def new_chunks_creator(file_name,subject):
        known_file_names = load_known_files()
        found = any(file['filename'] == file_name for file in known_file_names)
        if found:
            raise FileAlreadyExistsError("File already exists")
        text = file_opener(file_name)
        if not text or not text.strip():
            raise EmptyTextError("The text is Empty")
        dic_chunks = build_chunk_dicts(text)
        only_chunk = [chunk["chunk"] for chunk in dic_chunks]
        embeddings = gc.get_embedding(only_chunk)
        new_dic_chunks = [{"Index":dic_chunks[i]["Index"], "chunk": dic_chunks[i]["chunk"], "embedding": embeddings[i]} for i in range(len(dic_chunks))]
        known_file_names.append({"filename": file_name, "subject": subject})
        vs.add_chunks_to_collection(new_dic_chunks,subject=subject,file_name=file_name)
        save_known_files(known_file_names)
        return len(new_dic_chunks)

def main():
    while True:
        choice = menu()
        if choice == 1:
            if vs.collection.count() > 0:
                known_file_names = load_known_files()
                try:
                    if len(known_file_names) > 0:
                        print("Existing file names found in the collection:")
                        for index,files_names in enumerate(known_file_names):
                            print((index+1),".",files_names["filename"],"(",files_names["subject"],")")
                        
                        file_index = int(input("Enter the number of file you want to select:"))
                        file_chosen = known_file_names[file_index-1]["filename"]
                    else:
                        print("The notes collection is empty.")
                        continue
                    question = input("Enter your question: ")
                    relevant_chunk = query_collection(question, filename=file_chosen)
                    answer = gc.ask_gemini(question, relevant_chunk)
                    print("Answer:", answer)
                except ValueError:
                    print("Please enter a number")
                    continue
                except IndexError:
                    print("Please select an index within the given range")
                    continue
            else:
                print("No data in the collection. Please add a new file first.")
                continue
        elif choice == 2:
            file_name = input("Enter the name of the note file: ").strip().lower()
            subject = input("Enter the subject of the note: ")
            try:
                new_chunks_creator(file_name=file_name,subject=subject)
            except FileAlreadyExistsError as e:
                print(e)
            except EmptyTextError as e:
                print(e)
            except UnSupportedFileType as e:
                print(e)
        elif choice == 3:
            print("Exiting the program.")
            break
        elif choice is None:
            continue
        else:
            print("Invalid choice. Please try again.")
            continue
if __name__ == "__main__":
    main()