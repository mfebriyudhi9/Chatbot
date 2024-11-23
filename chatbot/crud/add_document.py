from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import Config
from uuid import uuid4
import os

from chatbot.parent import DocumentOperation


class DocumentAdder(DocumentOperation):
    def __init__(self, file_path):
        try:
            # Initialize the parent class
            super().__init__(file_path)
            # Initialize embeddings
            self.embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)
            # Initialize Chroma vector database
            self._vector_db = Chroma(
                client=self._client,
                collection_name=Config.CHROMA_COLLECTION,
                embedding_function=self.embedding
            )
        except Exception as e:
            print(f"Error initializing DocumentAdder: {e}")
            self._vector_db = None

    def add_document(self, text):
        if not self._vector_db:
            print("Error: Vector database is not initialized.")
            return False

        try:
            # Prepare documents with metadata
            documents = [Document(page_content=t, metadata={"source": self.file_path}) for t in text]
            # Generate unique IDs for the documents
            ids = [str(uuid4()) for _ in range(len(documents))]

            # Add documents to the vector database
            self.get_vector_db().add_documents(documents=documents, ids=ids)
            return True
        except Exception as e:
            print(f"Error adding documents to vector database: {e}")
            return False

    def get_vector_db(self):
        if not self._vector_db:
            print("Error: Vector database is not initialized.")
            return None
        return self._vector_db
