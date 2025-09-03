from read_file import Read_File_Json
from SelectLLM import classifier,llm_answer
import gradio as gr
from groq import Groq
import os
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain.text_splitter import RecursiveCharacterTextSplitter
from pathlib import Path

path = Path("make_data/vnexpress_thoi_su.json").parent
my_text = Read_File_Json(path).Read()
# Pipeline RAG
# ======================
def rag_pipeline(query: str):
    check = classifier(query)
    if "Yes" in check:
        print("yes")
        return llm_answer(query)
    else:
        print("no")
        docs = vectorstore.similarity_search(query, k=3)
        context = "\n\n".join(d.page_content for d in docs)
        return llm_answer(query, context)

# ======================
# Chuẩn bị data + vectorstore
# (Ở đây mình giả sử bạn đã có biến my_text chứa dữ liệu scrape)
# ======================

embedding_model = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
text_splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = text_splitter.create_documents([my_text])
vectorstore = Chroma.from_documents(docs, embedding_model, persist_directory="db_news")

# ======================
# Gradio UI
# ======================
def chat_interface(query):
    return rag_pipeline(query)

demo = gr.Interface(
    fn=chat_interface,
    inputs=gr.Textbox(lines=2, placeholder="Nhập câu hỏi của bạn..."),
    outputs="text",
    title="RAG Chatbot Tin tức",
    description="Nhập câu hỏi, hệ thống sẽ trả lời trực tiếp hoặc dùng RAG từ dữ liệu đã scrape."
) 

demo.launch()
