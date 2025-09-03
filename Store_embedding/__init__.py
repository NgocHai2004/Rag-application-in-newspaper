from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter

class Store_Embedding:
    def __init__(self,document):
        self.document = document
    
    def store(self):
        embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
        docs = text_splitter.create_documents([self.document])

        vectorstore = Chroma.from_documents(docs, embedding_model, persist_directory="db_news")
        