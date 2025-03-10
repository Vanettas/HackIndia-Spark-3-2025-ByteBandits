import firebase_admin
from firebase_admin import credentials, storage
import os

# Initialize Firebase Admin SDK
FIREBASE_CREDENTIALS_PATH = "firebase_credentials.json"

if not firebase_admin._apps:  # Prevent multiple initializations
    cred = credentials.Certificate(FIREBASE_CREDENTIALS_PATH)
    firebase_admin.initialize_app(cred, {
        "storageBucket": "your-firebase-project-id.appspot.com"
    })

def upload_to_firebase(file_path, file_name):
    """Uploads a file to Firebase Storage and returns its public URL."""
    bucket = storage.bucket()
    blob = bucket.blob(file_name)

    blob.upload_from_filename(file_path)
    blob.make_public()  # Make the file publicly accessible

    return {"file_url": blob.public_url, "message": "File uploaded to Firebase successfully!"}

# Test Firebase connection
if __name__ == "__main__":
    print("Testing Firebase Connection...")
    try:
        bucket = storage.bucket()
        print(f"✅ Firebase Storage Connected: {bucket.name}")
    except Exception as e:
        print(f"❌ Firebase Connection Failed: {e}")
