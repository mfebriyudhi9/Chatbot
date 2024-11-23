from langchain_chroma import Chroma
from langchain.embeddings import HuggingFaceEmbeddings
from langchain_core.documents import Document

from config import Config
from uuid import uuid4
import os

from chatbot.parent import DocumentOperation


class DocumentAdder(DocumentOperation):
    def __init__(self, file_path):
        super().__init__(file_path)
        self.embedding = HuggingFaceEmbeddings(model_name=Config.EMBEDDING_MODEL_NAME)

        self._vector_db = Chroma(
            client=self._client,
            collection_name=Config.CHROMA_COLLECTION,
            embedding_function=self.embedding            
        )

    def add_document(self, text):
        documents = [Document(page_content=t, metadata={"source": self.file_path}) for t in text]

        ids = [str(uuid4()) for _ in range(len(documents))]

        self.get_vector_db().add_documents(documents=documents, ids=ids)

        return True

    def get_vector_db(self):
        return self._vector_db
