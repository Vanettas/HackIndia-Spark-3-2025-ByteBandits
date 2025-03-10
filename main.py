from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from search import search_documents
from upload import upload_document
from googlehelper import list_google_drive_files

app = FastAPI()

# Auto-detect frontend URL
DEFAULT_FRONTEND_URL = "http://localhost:3000"
ALLOWED_ORIGINS = [DEFAULT_FRONTEND_URL]

app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.middleware("http")
async def detect_frontend_origin(request: Request, call_next):
    """Auto-detect frontend URL."""
    origin = request.headers.get("origin")
    if origin and origin not in ALLOWED_ORIGINS:
        ALLOWED_ORIGINS.append(origin)
    response = await call_next(request)
    return response

@app.get("/")
async def root():
    """Test API."""
    return {"message": f"FastAPI running with CORS for: {ALLOWED_ORIGINS}"}

@app.post("/api/search")
async def search_api(query: dict):
    """Search documents."""
    return search_documents(query["query"])

@app.post("/api/upload")
async def upload_api(document: dict):
    """Upload a document to MongoDB & Google Drive."""
    return upload_document(document["title"], document["content"], document["file_path"])

@app.get("/api/drive-files")
async def list_drive_files():
    """List files from Google Drive."""
    return list_google_drive_files()
