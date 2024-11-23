from langchain.chains import RetrievalQA
from langchain.embeddings import HuggingFaceEmbeddings

import os
import sys

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from config import Config
from database import DataBase

db = DataBase()
db.creat_table_if_not_exists()

class LLMRAG:
    def __init__(self):
        try:
            self.llm = Config.get_llm()
            self.prompt_template = Config.get_prompt_template()
            self.vector_db = Config.get_vector_db()

            self.conversation_retrieval_chain = RetrievalQA(
                llm=self.llm,
                chain_type="stuff",
                retriever=self.vector_db.as_retriever(search_mmr='mmr', search_kwargs={"k": 2}),
                return_source_documents=True
            )
        except Exception as e:
            print(f"Error initializing LLMRAG: {e}")
            self.conversation_retrieval_chain = None

    def process_prompt(self, prompt, uuid):
        if not self.conversation_retrieval_chain:
            print("Error: Conversation retrieval chain is not initialized.")
            return "Error processing the request. Please try again.", []

        try:
            # Format the prompt
            formatted_prompt = self.prompt_template.format(input=prompt)
        except Exception as e:
            print(f"Error formatting the prompt: {e}")
            return "Error processing the request. Please try again.", []

        try:
            # Retrieve chat history from the database
            chat_history = db.retrieve_chat_history(uuid, 10)
        except Exception as e:
            print(f"Error retrieving chat history: {e}")
            chat_history = ""

        try:
            # Process the prompt through the conversation chain
            output = self.conversation_retrieval_chain({
                "prompt": formatted_prompt,
                "chat_history": chat_history
            })
            answer = output.get('result', "Error generating the response.")
            source_documents = output.get('source_documents', [])

            # Save the conversation to the database
            try:
                db.save_to_database(prompt, answer, uuid)
            except Exception as e:
                print(f"Error saving chat to database: {e}")

            return answer, source_documents

        except Exception as e:
            print(f"Error processing the prompt: {e}")
            return "Error processing the request. Please try again.", []
