from transformers import pipeline
from sentence_transformers import SentenceTransformer, util

qa_pipeline = pipeline("question-answering")
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

def chunk_text(text, chunk_size=400):
    sentences = text.split(". ")
    chunks, chunk = [], ""
    for sentence in sentences:
        if len(chunk) + len(sentence) < chunk_size:
            chunk += sentence + ". "
        else:
            chunks.append(chunk.strip())
            chunk = sentence + ". "
    chunks.append(chunk.strip())
    return chunks

def answer_question(document_text, user_question):
    chunks = chunk_text(document_text)
    question_embedding = embedding_model.encode(user_question, convert_to_tensor=True)

    best_chunk = max(
        chunks,
        key=lambda x: util.pytorch_cos_sim(question_embedding, embedding_model.encode(x, convert_to_tensor=True)).item()
    )

    try:
        answer = qa_pipeline(question=user_question, context=best_chunk)
        return answer['answer'], f"Based on: '{best_chunk[:100]}...'"
    except Exception as e:
        return "Could not generate answer.", f"Error: {e}"
