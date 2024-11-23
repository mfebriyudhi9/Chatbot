import chromadb
from chatbot.parent import DocumentOperation

class DeleteDocument(DocumentOperation):
    def __init__(self,file_path):
        super().__init__(file_path)

    def delete_document(self):
        self._collection.delete(where={"source": self.file_path})
        return True
            

        
