# embeddings_manager.py
import os
import logging
import pickle
import numpy as np

class EmbeddingsManager:
    def __init__(self, embeddings_dir="data/embeddings"):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.embeddings_dir = embeddings_dir
        os.makedirs(self.embeddings_dir, exist_ok=True)
        
    def get_embeddings_path(self, doc_path):
        """Get the path where embeddings for a document would be stored"""
        doc_name = os.path.basename(doc_path)
        return os.path.join(self.embeddings_dir, f"{doc_name}.pkl")
        
    def has_embeddings(self, doc_path):
        """Check if embeddings exist for a document"""
        embeddings_path = self.get_embeddings_path(doc_path)
        return os.path.exists(embeddings_path)
    
    def save_embeddings(self, doc_path, embeddings):
        """Save embeddings for a document"""
        try:
            embeddings_path = self.get_embeddings_path(doc_path)
            with open(embeddings_path, 'wb') as f:
                pickle.dump(embeddings, f)
            logging.info(f"Saved embeddings for {doc_path}")
            return True
        except Exception as e:
            logging.error(f"Failed to save embeddings: {e}")
            return False
    
    def load_embeddings(self, doc_path):
        """Load embeddings for a document"""
        try:
            embeddings_path = self.get_embeddings_path(doc_path)
            if not os.path.exists(embeddings_path):
                return None
                
            with open(embeddings_path, 'rb') as f:
                return pickle.load(f)
        except Exception as e:
            logging.error(f"Failed to load embeddings: {e}")
            return None