from crud import DocumentAdder, DocumentUpdate, DeleteDocument
from config import Config

class DocsMasterProcess:
    def update(self, file_path):
        try:
            # Initialize processor and perform update
            processor = DocumentUpdate(file_path)
            extracted_text = processor.extract()
            processor.update_document(extracted_text)
            return True
        except Exception as e:
            print(f"Error during document update: {e}")
            return False

    def add(self, file_path):
        try:
            # Initialize processor and perform addition
            processor = DocumentAdder(file_path)
            extracted_text = processor.extract()
            processor.add_document(extracted_text)
            return True
        except Exception as e:
            print(f"Error during document addition: {e}")
            return False

    def delete(self, file_path):
        try:
            # Initialize processor and perform deletion
            processor = DeleteDocument(file_path)
            processor.delete_document()
            return True
        except Exception as e:
            print(f"Error during document deletion: {e}")
            return False
