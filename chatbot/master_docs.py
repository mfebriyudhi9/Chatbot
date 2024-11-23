from crud import DocumentAdder, DocumentUpdate, DeleteDocument
from config import Config

class DocsMasterProcess:
    def update(self, file_path) :
        processor = DocumentUpdate(file_path)
        extracted_text = processor.extract()
        processor.update_document(extracted_text)
        return True
    
    def add(self, file_path) :
        processor = DocumentAdder(file_path)
        extracted_text = processor.extract()
        processor.add_document(extracted_text)
        return True

    def delete(self, file_path) :
        processor = DeleteDocument(file_path)
        processor.delete_document()
        return True