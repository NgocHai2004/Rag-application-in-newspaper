import sys
import os
from llama_index.core import Document
# thêm path thủ công 
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from package import (
    pandas as pd,
    SentenceSplitter, 
    SimpleNodeParser
)

class Chuck():
    def __init__(self,document):
        self.document = document

    def chucking(self):
        documents = [Document(text=doc["content"]) for doc in self.document]
        text_splitter = SentenceSplitter(chunk_size=512, chunk_overlap=128)
        processed_documents = text_splitter(documents)
        return processed_documents
        
