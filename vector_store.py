import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(name="embedding_collection")

def add_chunks_to_collection(dic_chunks):
    document_para = [chunk["chunk"] for chunk in dic_chunks]
    ids = [str(chunk["Index"]) for chunk in dic_chunks]
    embeddings = [chunk["embedding"] for chunk in dic_chunks]

    collection.add(
        embeddings=embeddings,
        ids= ids,
        documents= document_para
    )
