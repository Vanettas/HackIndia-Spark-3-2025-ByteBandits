import os
import logging
import chardet
import docx
from PyPDF2 import PdfReader

class DocumentProcessor:
    def __init__(self):
        # Configure logging
        logging.basicConfig(level=logging.INFO)
        self.max_file_size = 50 * 1024 * 1024  # 50MB max file size
        
    def extract_text_from_file(self, file_path):
        """Extract text content from a file"""
        try:
            if not os.path.exists(file_path):
                return "File not found"
                
            ext = os.path.splitext(file_path)[1].lower()
            
            # Skip large files
            if os.path.getsize(file_path) > self.max_file_size:
                return "File too large to process"

            # Handle PDF files
            if ext == '.pdf':
                try:
                    text = ""
                    with open(file_path, 'rb') as file:
                        pdf = PdfReader(file)
                        for page in pdf.pages:
                            text += page.extract_text() or ""
                    return text
                except Exception as e:
                    logging.error(f"Error processing PDF: {e}")
                    return f"Could not extract text from PDF: {str(e)}"
            
            # Handle DOCX files
            elif ext == '.docx':
                try:
                    doc = docx.Document(file_path)
                    return "\n".join([p.text for p in doc.paragraphs])
                except Exception as e:
                    logging.error(f"Error processing DOCX: {e}")
                    return f"Could not extract text from DOCX: {str(e)}"
            
            # Handle TXT files
            elif ext == '.txt':
                try:
                    # Try to detect encoding
                    with open(file_path, 'rb') as f:
                        raw_data = f.read()
                        result = chardet.detect(raw_data)
                        encoding = result['encoding'] or 'utf-8'
                    
                    # Read with detected encoding
                    with open(file_path, 'r', encoding=encoding, errors='replace') as f:
                        return f.read()
                except Exception as e:
                    logging.error(f"Error processing TXT: {e}")
                    return f"Could not extract text from TXT: {str(e)}"
            
            return "Unsupported file format"
        except Exception as e:
            logging.error(f"Error extracting text: {e}")
            return f"Error processing file: {str(e)}"