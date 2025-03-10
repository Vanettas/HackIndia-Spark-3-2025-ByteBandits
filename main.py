
from fastapi import FastAPI, Request, UploadFile, File, Form, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from upload import upload_document
from search import search_documents
from summarizer import summarize_text  # Import AI Summarizer
import os

app = FastAPI()

# CORS Middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change this to specific frontend URL in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
async def root():
    """Test API."""
    return {"message": "FastAPI is running with MongoDB & Firebase!"}

@app.post("/api/upload")
async def upload_api(file: UploadFile = File(...), title: str = Form(...), content: str = Form(...)):
    """API to handle file uploads."""
    try:
        # Ensure upload directory exists
        os.makedirs("uploads", exist_ok=True)
        file_path = f"uploads/{file.filename}"

        # Save file locally
        with open(file_path, "wb") as buffer:
            buffer.write(file.file.read())

        # Upload document to Firebase & store metadata in MongoDB
        response = upload_document(title, content, file_path)

        # Delete the local file after uploading
        os.remove(file_path)

        return response

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Upload failed: {str(e)}")

@app.post("/api/search")
async def search_api(request: Request):
    """API to search documents."""
    try:
        query_data = await request.json()  # Ensure query is parsed correctly
        if "query" not in query_data:
            raise HTTPException(status_code=400, detail="Missing search query.")

        return search_documents(query_data["query"])

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Search failed: {str(e)}")


@app.post("/api/summarize")
async def summarize_api(request: Request):
    """API to summarize text."""
    try:
        data = await request.json()
        if "text" not in data:
            raise HTTPException(status_code=400, detail="Missing text input.")

        summary = summarize_text(data["text"])
        return {"summary": summary}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Summarization failed: {str(e)}")

