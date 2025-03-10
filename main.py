# import os
# import sys
# import streamlit as st
# import subprocess
# import argparse

# def setup_directory():
#     """Create necessary directories if they don't exist"""
#     os.makedirs("data/documents", exist_ok=True)
#     os.makedirs("data/vector_index", exist_ok=True)

# def process_initial_documents(initial_dir=None):
#     """Process documents in the specified directory"""
#     try:
#         from src.document_processor import DocumentProcessor
#         from src.embeddings_manager import EmbeddingsManager
        
#         # Use specified directory or default
#         doc_dir = initial_dir if initial_dir else "data/documents"
        
#         # Process documents
#         processor = DocumentProcessor(root_dir=doc_dir)
#         chunks = processor.process_all_documents()
        
#         # Create vector store
#         embeddings_manager = EmbeddingsManager()
#         vector_store = embeddings_manager.get_or_create_vector_store(chunks)
        
#         print("Successfully processed {len(chunks)} document chunks.")
        
#     except Exception as e:
#         print("Error processing documents: {str(e)}")

import streamlit as st
import os
import sys

# Ensure directories exist
os.makedirs("data/documents", exist_ok=True)
os.makedirs("data/vector_index", exist_ok=True)

# Run the Streamlit app
if __name__ == "__main__":
    # This is just an entry point - Streamlit will look for app.py
    # Run with: streamlit run main.py
    print("Starting Document Assistant...")