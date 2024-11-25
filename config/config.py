from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os

load_dotenv()

class Config:
    #chroma 
    CHROMADB_DIRECTORY = "VECTOR_DB"
    CHROMA_COLLECTION = "ISO"
    # CHROMA_COLLETION_METADATA = {"hnsw:space": "cosine"}
    TOTAL_K_RETURNED_DOCS = 2
    LLM_CONTEXT_LIMIT = 10

    LLM_API_KEY_ENV = os.getenv("GROQ_API_KEY") 
    LLM_MODEL_NAME = "Llama-3.1-70b-Versatile"
    EMBEDDING_MODEL_NAME = "sentence-transformers/all-MiniLM-L12-v2"

    PROMPT_TAMPLATE_MASSAGES = [
        ("system",
         "You are an assistant that are very proficient at answering user prompt regarding health, safety, environment (HSE) issues. also it is mandatory to give response in indonesian language, otherwise i'll punish you"),
         ("human", 
          "This is the user's prompts:\n\n {prompt}")
    ]

    PDF_FOLDER = "kumpulan_pdf"

    SECRET_KEY = "SPIL"

    @classmethod
    def get_prompt_template(cls):
        try:
            return ChatPromptTemplate.from_messages(cls.PROMPT_TAMPLATE_MASSAGES)
        except Exception as e:
            print(f"Error while getting prompt template: {e}")
            raise
        
    @classmethod
    def get_llm(cls):
        try:
            if cls.LLM_API_KEY_ENV is None:
                raise ValueError("GROQ_API_KEY is not set in enveronment variable.")
            return ChatGroq(groq_api_key=cls.LLM_API_KEY_ENV, model_name=cls.LLM_MODEL_NAME)
        except ValueError as ve:
            print(f"COnfiguration error: {str(ve)}")
            raise
        except Exception as e:
            print(f"Error initializing model : {str(e)}")
            raise


