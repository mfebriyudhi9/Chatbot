import chromadb
from chatbot.parent import DocumentOperation

class DeleteDocument(DocumentOperation):
    def __init__(self, file_path):
        try:
            # Initialize the parent class
            super().__init__(file_path)
        except Exception as e:
            print(f"Error initializing DeleteDocument: {e}")
            self._collection = None
            self.file_path = None

    def delete_document(self):
        if not self._collection:
            print("Error: Collection is not initialized.")
            return False

        try:
            # Attempt to delete the document from the collection
            self._collection.delete(where={"source": self.file_path})
            return True
        except Exception as e:
            print(f"Error deleting document with source '{self.file_path}': {e}")
            return False