import logging
from mongo import documents_collection
from search import model
from firebasehelper import upload_to_firebase  # Switched from Google Drive to Firebase
from summarizer import summarize_text  # Import AI Summarizer

# Set up logging
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")


def upload_document(title: str, content: str, local_file_path: str):
    """Uploads a document with AI-generated embedding & stores it in Firebase & MongoDB."""

    if not title or not content:
        logging.error("Title and content are required.")
        return {"error": "Title and content are required."}

    try:
        # Generate AI-powered embedding
        logging.info("Generating AI embedding...")
        embedding = model.encode(content).tolist()

        # AI-generated summary using NLP
        logging.info("Generating AI summary...")
        summary = summarize_text(content)

        # Upload file to Firebase Storage
        logging.info(f"Uploading '{title}' to Firebase...")
        firebase_upload = upload_to_firebase(local_file_path, title)

        if "file_url" not in firebase_upload:
            logging.error("Firebase upload failed.")
            return {"error": "Firebase upload failed."}

        file_url = firebase_upload["file_url"]

        # Save document metadata to MongoDB
        new_doc = {
            "title": title,
            "summary": summary,  # AI-powered summary
            "embedding": embedding,  # AI embedding
            "file_url": file_url,  # Firebase file URL
        }

        inserted_doc = documents_collection.insert_one(new_doc)

        logging.info(f"Document '{title}' uploaded successfully!")

        return {
            "message": "Document uploaded successfully!",
            "file_url": file_url,
            "document_id": str(inserted_doc.inserted_id),
        }

    except Exception as e:
        logging.error(f"Failed to upload document: {str(e)}")
        return {"error": f"Failed to upload document: {str(e)}"}
