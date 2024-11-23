from unstructured.partition.pdf import partition_pdf

class Extractor:
    def __init__(self, file_path):
        try:
            # Attempt to partition the PDF file
            self.element = partition_pdf(
                filename=file_path,
                strategy="hi_res",
                infer_table_structure=True,
                extract_images_in_pdf=False,
                model_name="yolox",
                chunking_strategy="by_title"
            )
        except Exception as e:
            print(f"Error partitioning PDF file '{file_path}': {e}")
            self.element = None  # Fallback to indicate initialization failure

    def parse_element(self):
        # Check if partitioning succeeded
        if not self.element:
            print("Error: No elements to parse due to previous initialization failure.")
            return []

        try:
            # Attempt to parse elements
            text = []

            for e in self.element:
                if 'Table' in str(type(e)):
                    print(e.metadata.text_as_html)
                    text.append(e.metadata.text_as_html)
                else:
                    print(e)
                    text.append(e.text)

            return text
        except Exception as e:
            print(f"Error parsing elements: {e}")
            return []  # Return empty list on failure
