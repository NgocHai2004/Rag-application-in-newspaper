from groq import Groq
import os

os.environ["GROQ_API_KEY"] = "###"   # đổi key của bạn
client = Groq(api_key=os.environ["GROQ_API_KEY"])
def classifier(query: str):
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[
            {"role": "system", "content": "Bạn là trợ lý AI. Hãy phân tích xem có thể trả lời câu hỏi này bằng kiến thức có sẵn (Yes/No)."},
            {"role": "user", "content": query}
        ]
    )
    return resp.choices[0].message.content.strip()


def llm_answer(query: str, context: str = ""):
    messages = [
        {"role": "system", "content": "Bạn là trợ lý AI. Trả lời ngắn gọn, rõ ràng."},
        {"role": "user", "content": f"Câu hỏi: {query}\n\nNgữ cảnh:\n{context}"}
    ]
    resp = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=messages
    )
    return resp.choices[0].message.content.strip()
