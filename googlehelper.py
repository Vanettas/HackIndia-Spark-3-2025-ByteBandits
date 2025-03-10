import os
from google.oauth2 import service_account
from googleapiclient.discovery import build
from googleapiclient.http import MediaFileUpload

# Load Google API credentials
SERVICE_ACCOUNT_FILE = "credentials.json"  # Download this from Google Cloud Console
SCOPES = ["https://www.googleapis.com/auth/drive.file"]

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

drive_service = build("drive", "v3", credentials=credentials)


def upload_to_google_drive(file_path, file_name, folder_id=None):
    """Uploads a document to Google Drive."""
    file_metadata = {"name": file_name}
    if folder_id:
        file_metadata["parents"] = [folder_id]

    media = MediaFileUpload(file_path, resumable=True)
    file = drive_service.files().create(body=file_metadata, media_body=media, fields="id").execute()

    return file.get("id")


def list_google_drive_files():
    """Lists files from Google Drive."""
    results = drive_service.files().list(pageSize=10, fields="files(id, name)").execute()
    return results.get("files", [])
