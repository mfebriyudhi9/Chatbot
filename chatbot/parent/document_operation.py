import chromadb
from langchain_chroma import Chroma

from config import Config
from chatbot.utils import Extractor

import os


class DocumentOperation:
    def __init__(self, file_path):
        self._client = chromadb.PersistentClient(path=Config.CHROMADB_DIRECTORY)
        self._collection = self._client.get_collection(Config.CHROMA_COLLECTION)
        self.file_path = os.path.join(Config.PDF_FOLDER, file_path)

    def extract(self):
        text = Extractor(self.file_path).parse_element()
        return text
    
    

