from read_file import Read_File_Json
from clean_chuck import Chuck
import torch
from llama_index.embeddings.huggingface import HuggingFaceEmbedding
def main():
    df = Read_File_Json("make_data/vnexpress_thoi_su.json").Read()
    text = Chuck(df).chucking()
    device = "cuda" if torch.cuda.is_available() else "cpu"
    embed_model = HuggingFaceEmbedding(model_name="BAAI/bge-small-en-v1.5", device=device)
    embeddings = [embed_model.get_text_embedding(chunk.text) for chunk in text]
    print(embeddings[0])   

main()