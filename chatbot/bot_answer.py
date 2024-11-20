from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings


import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from config import Config

class LLMRAG:
    def __init__(self):
        self.llm = Config.get_llm()
        self.prompt_template = Config.get_prompt_template()
        self.vector_db = Config.get_vector_db()

        self.conversation_retrieval_chain = RetrievalQA(
            llm=self.llm,
            chain_type="stuff",
            retriever=self.vector_db.as_retriever(search_mmr='mmr', search_kwargs={"k": 2}),
            return_source_documents=True
        )

    def process_prompt(self, prompt, uuid):
        formatted_prompt = self.prompt_template.format(input=prompt)
        chat_history = self.retrieve_chat_history(uuid)

        output = self.conversation_retrieval_chain({"prompt":prompt, 'chat_history': chat_history})
        answer = output['result']
        source_documents = output['source_documents']

        # add function to save to db

        return answer, source_documents