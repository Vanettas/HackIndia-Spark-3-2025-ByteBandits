# import os
# import glob
# from collections import defaultdict
# import logging

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# class DocumentNavigator:
#     def __init__(self, root_dir="data/documents"):
#         self.root_dir = root_dir
#         self.file_structure = None

#     def scan_file_structure(self):
#         """Scan and return document file structure"""
#         self.file_structure = defaultdict(list)
#         supported_files = ['.pdf', '.txt', '.docx']
        
#         all_files = []
#         for ext in supported_files:
#             all_files.extend(glob.glob(f"{self.root_dir}/**/*{ext}", recursive=True))

#         for file_path in all_files:
#             folder = os.path.dirname(file_path)
#             self.file_structure[folder].append({
#                 'file_name': os.path.basename(file_path),
#                 'file_path': file_path
#             })

#         logging.info(f"Found {len(all_files)} documents.")
#         return self.file_structure




# import os
# import glob
# import logging
# from pathlib import Path
# import win32api
# import win32con
# import win32file
# import string

# # Configure logging
# logging.basicConfig(level=logging.INFO)

# class DocumentNavigator:
#     def __init__(self, root_dir="data/documents"):
#         self.root_dir = root_dir
#         os.makedirs(self.root_dir, exist_ok=True)
#         self.supported_exts = ['.pdf', '.txt', '.docx']

#     # def get_document_list(self):
#     #     """Get a list of document filenames from the project directory"""
#     #     all_files = []
#     #     for ext in self.supported_exts:
#     #         all_files.extend(glob.glob(f"{self.root_dir}/*{ext}"))
#     #     return [os.path.basename(f) for f in all_files]

#     def get_document_list(self):
#         """Get a list of document filenames from the project directory"""
#         all_files = []
#         for ext in self.supported_exts:
#             all_files.extend(glob.glob(f"{self.root_dir}/*{ext}"))
#         return [os.path.basename(f) for f in all_files]

#     def get_drives(self):
#         """Get all available drives on Windows"""
#         drives = []
#         bitmask = win32api.GetLogicalDrives()
#         for letter in string.ascii_uppercase:
#             if bitmask & 1:
#                 drives.append(f"{letter}:\\")
#             bitmask >>= 1
#         return drives

#     def search_system_documents(self, query):
#         """Search for documents across the entire system"""
#         system_docs = []
#         query = query.lower()
        
#         # Get all drives
#         drives = self.get_drives()
        
#         # Common folders to search (add more as needed)
#         common_folders = [
#             "Documents",
#             "Downloads",
#             "Desktop",
#             "Pictures",
#             "Videos",
#             "Music",
#             "OneDrive",
#             "Dropbox",
#             "Google Drive"
#         ]
        
#         # Search in user's home directory and common folders
#         user_home = str(Path.home())
#         search_paths = [user_home]
        
#         # Add common folders under user's home
#         for folder in common_folders:
#             path = os.path.join(user_home, folder)
#             if os.path.exists(path):
#                 search_paths.append(path)
        
#         # Search in all drives
#         for drive in drives:
#             try:
#                 # Search in root of each drive
#                 for ext in self.supported_exts:
#                     try:
#                         files = glob.glob(f"{drive}**/*{ext}", recursive=True)
#                         for file_path in files:
#                             try:
#                                 # Check if file is accessible
#                                 if os.access(file_path, os.R_OK):
#                                     doc_name = os.path.basename(file_path)
#                                     # Search in both filename and content
#                                     if query in doc_name.lower():
#                                         system_docs.append({
#                                             'name': doc_name,
#                                             'path': file_path,
#                                             'type': 'system',
#                                             'location': os.path.dirname(file_path)
#                                         })
#                             except Exception as e:
#                                 logging.warning(f"Error accessing file {file_path}: {e}")
#                                 continue
#                     except Exception as e:
#                         logging.warning(f"Error searching in drive {drive}: {e}")
#                         continue
#             except Exception as e:
#                 logging.warning(f"Error processing drive {drive}: {e}")
#                 continue
        
#         # Search in user's home directory and common folders
#         for search_path in search_paths:
#             try:
#                 for ext in self.supported_exts:
#                     try:
#                         files = glob.glob(f"{search_path}/**/*{ext}", recursive=True)
#                         for file_path in files:
#                             try:
#                                 if os.access(file_path, os.R_OK):
#                                     doc_name = os.path.basename(file_path)
#                                     if query in doc_name.lower():
#                                         system_docs.append({
#                                             'name': doc_name,
#                                             'path': file_path,
#                                             'type': 'system',
#                                             'location': os.path.dirname(file_path)
#                                         })
#                             except Exception as e:
#                                 logging.warning(f"Error accessing file {file_path}: {e}")
#                                 continue
#                     except Exception as e:
#                         logging.warning(f"Error searching in {search_path}: {e}")
#                         continue
#             except Exception as e:
#                 logging.warning(f"Error processing path {search_path}: {e}")
#                 continue
        
#         return system_docs

#     # def scan_file_structure(self):
#     #     """Scan and return document file structure"""
#     #     file_structure = {}
#     #     all_files = []
        
#     #     # Scan project directory
#     #     for ext in self.supported_exts:
#     #         all_files.extend(glob.glob(f"{self.root_dir}/**/*{ext}", recursive=True))
        
#     #     for file_path in all_files:
#     #         folder = os.path.dirname(file_path)
#     #         if folder not in file_structure:
#     #             file_structure[folder] = []
            
#     #         file_structure[folder].append({
#     #             'file_name': os.path.basename(file_path),
#     #             'file_path': file_path,
#     #             'type': 'project'
#     #         })
        
#     #     logging.info(f"Found {len(all_files)} documents in project directory.")
#     #     return file_structure
#     def scan_file_structure(self):
#         """Scan and return document file structure"""
#         file_structure = {}
#         all_files = []
        
#         # Scan project directory
#         for ext in self.supported_exts:
#             all_files.extend(glob.glob(f"{self.root_dir}/**/*{ext}", recursive=True))
        
#         for file_path in all_files:
#             folder = os.path.dirname(file_path)
#             if folder not in file_structure:
#                 file_structure[folder] = []
            
#             file_structure[folder].append({
#                 'file_name': os.path.basename(file_path),
#                 'file_path': file_path,
#                 'type': 'project'
#             })
        
#         logging.info(f"Found {len(all_files)} documents in project directory.")
#         return file_structure




import os
import glob
import logging
from pathlib import Path
import win32api
import win32con
import win32file
import string

# Configure logging
logging.basicConfig(level=logging.INFO)

class DocumentNavigator:
    def __init__(self, root_dir="data/documents"):
        self.root_dir = root_dir
        os.makedirs(self.root_dir, exist_ok=True)
        self.supported_exts = ['.pdf', '.txt', '.docx']

    def get_document_list(self):
        """Get a list of document filenames from the project directory"""
        all_files = []
        for ext in self.supported_exts:
            all_files.extend(glob.glob(f"{self.root_dir}/*{ext}"))
        return [os.path.basename(f) for f in all_files]

    def get_drives(self):
        """Get all available drives on Windows"""
        drives = []
        bitmask = win32api.GetLogicalDrives()
        for letter in string.ascii_uppercase:
            if bitmask & 1:
                drives.append(f"{letter}:\\")
            bitmask >>= 1
        return drives

    def search_system_documents(self, query):
        """Search for documents across the entire system"""
        system_docs = []
        query = query.lower()
        
        # Get all drives
        drives = self.get_drives()
        
        # Common folders to search (add more as needed)
        common_folders = [
            "Documents",
            "Downloads",
            "Desktop",
            "Pictures",
            "Videos",
            "Music",
            "OneDrive",
            "Dropbox",
            "Google Drive"
        ]
        
        # Search in user's home directory and common folders
        user_home = str(Path.home())
        search_paths = [user_home]
        
        # Add common folders under user's home
        for folder in common_folders:
            path = os.path.join(user_home, folder)
            if os.path.exists(path):
                search_paths.append(path)
        
        # Search in all drives
        for drive in drives:
            try:
                # Search in root of each drive
                for ext in self.supported_exts:
                    try:
                        files = glob.glob(f"{drive}**/*{ext}", recursive=True)
                        for file_path in files:
                            try:
                                # Check if file is accessible
                                if os.access(file_path, os.R_OK):
                                    doc_name = os.path.basename(file_path)
                                    # Search in both filename and content
                                    if query in doc_name.lower():
                                        system_docs.append({
                                            'name': doc_name,
                                            'path': file_path,
                                            'type': 'system',
                                            'location': os.path.dirname(file_path)
                                        })
                            except Exception as e:
                                logging.warning(f"Error accessing file {file_path}: {e}")
                                continue
                    except Exception as e:
                        logging.warning(f"Error searching in drive {drive}: {e}")
                        continue
            except Exception as e:
                logging.warning(f"Error processing drive {drive}: {e}")
                continue
        
        # Search in user's home directory and common folders
        for search_path in search_paths:
            try:
                for ext in self.supported_exts:
                    try:
                        files = glob.glob(f"{search_path}/**/*{ext}", recursive=True)
                        for file_path in files:
                            try:
                                if os.access(file_path, os.R_OK):
                                    doc_name = os.path.basename(file_path)
                                    if query in doc_name.lower():
                                        system_docs.append({
                                            'name': doc_name,
                                            'path': file_path,
                                            'type': 'system',
                                            'location': os.path.dirname(file_path)
                                        })
                            except Exception as e:
                                logging.warning(f"Error accessing file {file_path}: {e}")
                                continue
                    except Exception as e:
                        logging.warning(f"Error searching in {search_path}: {e}")
                        continue
            except Exception as e:
                logging.warning(f"Error processing path {search_path}: {e}")
                continue
        
        return system_docs

    def scan_file_structure(self):
        """Scan and return document file structure"""
        file_structure = {}
        all_files = []
        
        # Scan project directory
        for ext in self.supported_exts:
            all_files.extend(glob.glob(f"{self.root_dir}/**/*{ext}", recursive=True))
        
        for file_path in all_files:
            folder = os.path.dirname(file_path)
            if folder not in file_structure:
                file_structure[folder] = []
            
            file_structure[folder].append({
                'file_name': os.path.basename(file_path),
                'file_path': file_path,
                'type': 'project'
            })
        
        logging.info(f"Found {len(all_files)} documents in project directory.")
        return file_structure