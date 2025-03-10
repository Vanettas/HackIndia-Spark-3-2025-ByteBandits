from sentence_transformers import SentenceTransformer
from mongo import documents_collection  # Import MongoDB connection

# Load NLP Model (Sentence Transformers)
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_documents(query_text):
    """Performs AI-powered document search in MongoDB."""
    if not query_text or not query_text.strip():
        return {"error": "Query text is required."}

    # Ensure MongoDB connection is available
    if documents_collection is None:
        return {"error": "Database connection failed. Please check MongoDB."}

    try:
        # Generate AI-powered embedding for the query
        query_embedding = model.encode(query_text).tolist()

        # Fetch all documents from MongoDB
        # documents = list(documents_collection.find({}, {"_id": 0, "title": 1, "summary": 1, "embedding": 1}))
        #
        # if not documents:
        #     return {"error": "No documents found in database."}
        #
        # # Filter out documents with missing or invalid embeddings
        # valid_documents = [doc for doc in documents if "embedding" in doc and isinstance(doc["embedding"], list)]
        #
        # if not valid_documents:
        #     return {"error": "No valid embeddings found in documents."}
        #
        # # Compute similarity scores
        # for doc in valid_documents:
        #     doc["score"] = sum(a * b for a, b in zip(doc["embedding"], query_embedding))
        #
        # # Sort documents by highest relevance
        # valid_documents.sort(key=lambda x: x["score"], reverse=True)

        # Fetch documents containing the query text (MongoDB text search)
        text_query = {"$text": {"$search": query_text}}  # MongoDB Full-Text Search
        text_documents = list(
            documents_collection.find(text_query, {"_id": 0, "title": 1, "summary": 1, "embedding": 1}))

        # Fetch all documents for similarity comparison
        all_documents = list(documents_collection.find({}, {"_id": 0, "title": 1, "summary": 1, "embedding": 1}))

        # Compute similarity scores
        for doc in all_documents:
            if "embedding" in doc and isinstance(doc["embedding"], list):
                doc["score"] = sum(a * b for a, b in zip(doc["embedding"], query_embedding))
            else:
                doc["score"] = 0  # Handle missing embeddings

        # Sort AI-based results by highest similarity score
        all_documents.sort(key=lambda x: x["score"], reverse=True)

        # Combine text search and AI similarity results
        combined_results = text_documents + [doc for doc in all_documents if doc not in text_documents]
        return {"documents": combined_results[:5]}
        # return {"documents": valid_documents[:5]}  # Return top 5 relevant documents

    except Exception as e:
        return {"error": f"An error occurred during search: {str(e)}"}
