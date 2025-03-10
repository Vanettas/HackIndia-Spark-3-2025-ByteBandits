from mongo import documents_collection
from search import model
from googlehelper import upload_to_google_drive
from summarizer import summarize_text  # Import AI Summarizer


def upload_document(title: str, content: str, local_file_path: str):
    """Uploads a document with AI-generated embedding & stores it on Google Drive."""

    if not title or not content:
        return {"error": "Title and content are required."}

    try:
        # Generate AI-powered embedding
        embedding = model.encode(content).tolist()

        # AI-generated summary using NLP
        summary = summarize_text(content)

        # Upload file to Google Drive
        drive_upload = upload_to_google_drive(local_file_path, title)

        if "file_id" not in drive_upload:
            return {"error": "Google Drive upload failed."}

        google_drive_file_id = drive_upload["file_id"]

        # Save document to MongoDB
        new_doc = {
            "title": title,
            "summary": summary,  # AI-powered summary
            "embedding": embedding,  # AI embedding
            "google_drive_id": google_drive_file_id,  # Drive file ID
        }

        inserted_doc = documents_collection.insert_one(new_doc)

        return {
            "message": "Document uploaded successfully!",
            "drive_id": google_drive_file_id,
            "document_id": str(inserted_doc.inserted_id),
        }

    except Exception as e:
        return {"error": f"Failed to upload document: {str(e)}"}
