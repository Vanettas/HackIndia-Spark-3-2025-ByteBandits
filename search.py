from sentence_transformers import SentenceTransformer
from mongo import documents_collection  # Import MongoDB connection

# Load NLP Model (Sentence Transformers)
model = SentenceTransformer("all-MiniLM-L6-v2")

def search_documents(query_text):
    """Performs AI-powered document search in MongoDB."""
    if not query_text.strip():
        return {"error": "Query text is required"}

    query_embedding = model.encode(query_text).tolist()

    # Fetch all documents
    documents = list(documents_collection.find({}, {"_id": 0, "title": 1, "summary": 1, "embedding": 1}))

    # Compute similarity scores
    for doc in documents:
        doc["score"] = sum(a * b for a, b in zip(doc["embedding"], query_embedding))

    # Sort documents by relevance
    documents.sort(key=lambda x: x["score"], reverse=True)

    return {"documents": documents[:5]}  # Return top 5 results
