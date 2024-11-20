from unstructured.partition.pdf import partition_pdf

class Extractor:
    def __init__(self, file_path):


        self.element = partition_pdf(
                    filename=file_path,
                    strategy="hi_res",
                    infer_table_structure=True,
                    extract_images_in_pdf=False,
                    model_name="yolox",
                    chunking_strategy="by_title"
        )

    def parse_element(self):
        text = []

        for e in self.element:
            if 'Table' in str(type(e)):
                print(e.metadata.text_as_html)
                text.append(e.metadata.text_as_html)
            else:
                print(e)
                text.append(e.text)

        return text
            