import chromadb
from langchain_chroma import Chroma

from config import Config
from chatbot.utils import Extractor

import os

class DocumentOperation:
    def __init__(self, file_path):
        try:
            # Initialize ChromaDB client and collection
            self._client = chromadb.PersistentClient(path=Config.CHROMADB_DIRECTORY)
            self._collection = self._client.get_collection(Config.CHROMA_COLLECTION)
            self.file_path = os.path.join(Config.PDF_FOLDER, file_path)
        except Exception as e:
            print(f"Error initializing DocumentOperation: {e}")
            self._client = None
            self._collection = None
            self.file_path = None

    def extract(self):
        if not self.file_path:
            print("Error: Invalid file path or initialization failed.")
            return None

        try:
            # Extract text from the file
            text = Extractor(self.file_path).parse_element()
            return text
        except Exception as e:
            print(f"Error extracting text from file '{self.file_path}': {e}")
            return None
