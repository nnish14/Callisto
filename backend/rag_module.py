# rag_module.py

from sentence_transformers import SentenceTransformer
import faiss
import numpy as np
import pickle
import os

# Paths for storing the FAISS index and metadata
INDEX_FILE = "../data/rag_index.faiss"
METADATA_FILE = "../data/rag_metadata.pkl"

class RAGMemory:
    def __init__(self):
        # Initialize the embedding model
        self.embedder = SentenceTransformer("all-MiniLM-L6-v2")
        self.dimension = 384  # Dimension of embeddings from all-MiniLM-L6-v2
        
        # Initialize FAISS index
        self.index = faiss.IndexFlatL2(self.dimension)
        
        # Store metadata (text and additional info)
        self.metadata = []
        
        # Load existing index and metadata if they exist
        self._load()

    def _load(self):
        """Loads the FAISS index and metadata from disk if they exist."""
        if os.path.exists(INDEX_FILE) and os.path.exists(METADATA_FILE):
            self.index = faiss.read_index(INDEX_FILE)
            with open(METADATA_FILE, "rb") as f:
                self.metadata = pickle.load(f)

    def _save(self):
        """Saves the FAISS index and metadata to disk."""
        os.makedirs(os.path.dirname(INDEX_FILE), exist_ok=True)
        faiss.write_index(self.index, INDEX_FILE)
        with open(METADATA_FILE, "wb") as f:
            pickle.dump(self.metadata, f)

    def add_to_memory(self, text: str, metadata: dict) -> None:
        """
        Adds text to the RAG memory with metadata.
        :param text: The text to embed and store.
        :param metadata: Metadata associated with the text (e.g., timestamp, user_input).
        """
        # Generate embedding
        embedding = self.embedder.encode([text])[0]
        
        # Add to FAISS index
        self.index.add(np.array([embedding], dtype=np.float32))
        
        # Store metadata
        self.metadata.append({"text": text, **metadata})
        
        # Save to disk
        self._save()

    def retrieve_relevant_context(self, query: str, k: int = 3) -> list:
        """
        Retrieves the top k relevant pieces of context for a query.
        :param query: The query text.
        :param k: Number of results to return.
        :return: List of relevant texts and their metadata.
        """
        if self.index.ntotal == 0:
            return []
        
        # Generate query embedding
        query_embedding = self.embedder.encode([query])[0]
        
        # Search for the top k similar embeddings
        distances, indices = self.index.search(np.array([query_embedding], dtype=np.float32), k)
        
        # Retrieve the corresponding texts and metadata
        results = []
        for idx in indices[0]:
            if idx != -1 and idx < len(self.metadata):  # Check for valid indices
                results.append(self.metadata[idx])
        return results

if __name__ == "__main__":
    # Test the RAG system
    rag = RAGMemory()
    rag.add_to_memory("Hello, how are you?", {"timestamp": "2025-03-21 12:00:00", "type": "user"})
    rag.add_to_memory("Hi! I'm doing great, thanks for asking.", {"timestamp": "2025-03-21 12:00:01", "type": "assistant"})
    rag.add_to_memory("I need help with first aid.", {"timestamp": "2025-03-21 12:01:00", "type": "user"})
    
    # Retrieve relevant context
    query = "Tell me about first aid."
    relevant_context = rag.retrieve_relevant_context(query, k=2)
    print(f"Query: {query}")
    print("Relevant context:")
    for item in relevant_context:
        print(f"- {item['text']} (Timestamp: {item['timestamp']}, Type: {item['type']})")