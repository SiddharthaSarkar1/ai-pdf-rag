import chromadb
from sentence_transformers import SentenceTransformer

class ChromaRAG:
    def __init__(self):
        # Creating a persistent chroma database on disk
        self.client = chromadb.PersistentClient(path="./chroma_store")

        #Embedding Model
        self.embeder = SentenceTransformer("all-MiniLM-L6-v2")

        # Start with a clean collection
        self.reset_collection()

    def reset_collection(self):
        try:
            self.client.delete_collection("docs")
        except:
            pass

        self.collection = self.client.create_collection("docs")


    def build(self, chunks):
        """ Create embeddings and store them in chroma """
        self.reset_collection()

        embeddings = self.embeder.encode(chunks).tolist()
        ids = [str(i) for i in range(len(chunks))]

        self.collection.add(
            ids = ids,
            embeddings=embeddings,
            documents=chunks,
        )

    def search(self, query, top_k=4):
        """ Return the most relevant chunks for a given query """
        query_embedding = self.embeder.encode([query]).tolist()[0]
        results = self.collection.query(
            query_embeddings=query_embedding,
            n_results=top_k
        )

        # Return list of documents
        return results["documents"][0]