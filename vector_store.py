import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="embedding_collection")

def add_chunks_to_collection(dic_chunks,file_name,subject=None):
    document_para = [chunk["chunk"] for chunk in dic_chunks]
    ids = [(f"{file_name}_{chunk['Index']}") for chunk in dic_chunks]
    embeddings = [chunk["embedding"] for chunk in dic_chunks]
    metadatas = [{"subject":subject,"filename":file_name} for chunk in dic_chunks]


    collection.add(
        embeddings=embeddings,
        ids= ids,
        documents= document_para,
        metadatas=metadatas
    )
