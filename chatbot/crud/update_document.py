from config import Config
import os
from chatbot.parent import DocumentOperation

class DocumentUpdate(DocumentOperation):
    def __init__(self, file_path):
        try:
            # Initialize the parent class
            super().__init__(file_path)
        except Exception as e:
            print(f"Error initializing DocumentUpdate: {e}")
            self._collection = None
            self.file_path = None

    def update_document(self, text):
        if not self._collection:
            print("Error: Collection is not initialized.")
            return False

        try:
            # Update documents in the collection
            self._collection.update(
                document=[t for t in text],
                metadatas=[{"source": self.file_path}]
            )
            return True
        except Exception as e:
            print(f"Error updating document with source '{self.file_path}': {e}")
            return False