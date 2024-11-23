from config import Config
import os

from chatbot.parent import DocumentOperation

class DocumentUpdate(DocumentOperation):
    def __init__(self, file_path):
        super().__init__(file_path)                    

    def update_document(self, text):
        # file_path = os.path.join(Config.PDF_FOLDER, filename)
        self._collection.update(
            document=[t for t in text],
            metadatas=[{"source": self.file_path}]
        )

        return True