import chromadb
from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from utils import Extractor
from config import Config
from uuid import uuid4

import os

class DocumentAdder:
    def __init__(self):
        self.client = chromadb.PersistentClient(path=Config.CHROMADB_DIRECTORY)
        self.embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)

        self._vector_db = Chroma(
            client=self.client,
            collection_name=Config.CHROMA_COLLECTION,
            embedding_function=self.embedding            
        )

    def extract(self, file_path):
        text = Extractor(file_path).parse_element()
        return text

    def add_document(self, text, filename):
        file_path = os.path.join(Config.UPLOAD_DIRECTORY, filename)
        documents = [Document(page_content=t, metadata={"source": file_path}) for t in text]


        ids = [str(uuid4()) for _ in range(len(documents))]

        self.get_vector_db().add_documents(documents=documents, ids=ids)

    def get_vector_db(self):
        """Getter method to fetch the vector database."""
        return self._vector_db
