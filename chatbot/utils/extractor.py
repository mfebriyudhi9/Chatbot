from unstructured.partition.pdf import partition_pdf

class Extractor:
    def __init__(self, file_path):
        

        self.elements = partition_pdf(
            filename=file_path,
            strategy="hi_res",
            infer_table_structure=True,
            extract_images_in_pdf=True,
            model_name="yolox"
            )