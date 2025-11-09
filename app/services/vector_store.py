import logging
import os
import pickle
from typing import List, Dict, Any, Optional
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity

logger = logging.getLogger(__name__)


class VectorStoreService:    

    def __init__(self, persist_directory: str = "./chroma_db", collection_name: str = "architecture_docs"):
        self.persist_directory = persist_directory
        self.collection_name = collection_name
        self.persist_file = os.path.join(persist_directory, f"{collection_name}.pkl")
        
        # Create persist directory if it doesn't exist
        os.makedirs(persist_directory, exist_ok=True)
        
        # Initialize storage
        self.documents = []
        self.embeddings = []
        self.metadatas = []
        self.ids = []
        
        # Try to load existing data
        self._load_from_disk()
        
        logger.info(f"Initialized vector store: {collection_name}")
        logger.info(f"Collection contains {len(self.documents)} documents")
    
    def _load_from_disk(self):
        if os.path.exists(self.persist_file):
            try:
                with open(self.persist_file, 'rb') as f:
                    data = pickle.load(f)
                    self.documents = data.get('documents', [])
                    self.embeddings = data.get('embeddings', [])
                    self.metadatas = data.get('metadatas', [])
                    self.ids = data.get('ids', [])
                logger.info(f"Loaded {len(self.documents)} documents from disk")
            except Exception as e:
                logger.warning(f"Could not load persisted data: {str(e)}")
    
    def _save_to_disk(self):
        try:
            data = {
                'documents': self.documents,
                'embeddings': self.embeddings,
                'metadatas': self.metadatas,
                'ids': self.ids
            }
            with open(self.persist_file, 'wb') as f:
                pickle.dump(data, f)
            logger.info(f"Persisted {len(self.documents)} documents to disk")
        except Exception as e:
            logger.error(f"Error persisting data: {str(e)}")
    
    def count(self) -> int:
        # Get number of documents in the collection
        return len(self.documents)
    
    def add_documents(self, documents: List[Dict[str, Any]], gemini_service) -> None:
        try:
            # Check if collection already has documents
            if len(self.documents) > 0:
                logger.info(f"Collection already contains {len(self.documents)} documents. Skipping indexing.")
                return
            
            logger.info(f"Adding {len(documents)} documents to vector store...")
            
            # Extract texts for embedding
            texts = [doc['text'] for doc in documents]
            
            # Generate embeddings using Gemini
            logger.info("Generating embeddings with Gemini...")
            embeddings = gemini_service.generate_embeddings_batch(texts)
            
            # Store documents
            self.documents = texts
            self.embeddings = embeddings
            self.metadatas = [doc.get('metadata', {}) for doc in documents]
            self.ids = [f"doc_{i}" for i in range(len(documents))]
            
            # Persist to disk
            self._save_to_disk()
            
            logger.info(f"Successfully added {len(documents)} documents to vector store")
            
        except Exception as e:
            logger.error(f"Error adding documents to vector store: {str(e)}")
            raise
    
    def query(
        self,
        query_embedding: List[float],
        n_results: int = 5
    ) -> Dict[str, Any]:
        try:
            if len(self.embeddings) == 0:
                logger.warning("Vector store is empty")
                return {
                    'documents': [],
                    'distances': [],
                    'metadatas': []
                }
            
            # Convert to numpy arrays
            query_vec = np.array(query_embedding).reshape(1, -1)
            embeddings_matrix = np.array(self.embeddings)
            
            # Calculate cosine similarity
            similarities = cosine_similarity(query_vec, embeddings_matrix)[0]
            
            # Get top k indices
            top_indices = np.argsort(similarities)[::-1][:n_results]
            
            # Prepare results
            results_docs = [self.documents[i] for i in top_indices]
            results_distances = [float(1 - similarities[i]) for i in top_indices]  # Convert similarity to distance
            results_metadatas = [self.metadatas[i] for i in top_indices]
            
            logger.info(f"Retrieved {len(results_docs)} documents from vector store")
            
            return {
                'documents': results_docs,
                'distances': results_distances,
                'metadatas': results_metadatas
            }
            
        except Exception as e:
            logger.error(f"Error querying vector store: {str(e)}")
            raise
    
    def clear_collection(self) -> None:
        """Clear all documents from the collection"""
        try:
            self.documents = []
            self.embeddings = []
            self.metadatas = []
            self.ids = []
            
            # Remove persisted file
            if os.path.exists(self.persist_file):
                os.remove(self.persist_file)
            
            logger.info(f"Cleared collection: {self.collection_name}")
        except Exception as e:
            logger.error(f"Error clearing collection: {str(e)}")
            raise
    
    def get_collection_stats(self) -> Dict[str, Any]:
        """Get statistics about the collection"""
        return {
            "name": self.collection_name,
            "count": len(self.documents),
            "persist_directory": self.persist_directory
        }
