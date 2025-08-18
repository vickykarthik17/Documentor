from transformers import pipeline

summarizer = pipeline("summarization")

def generate_summary(text):
    if not text.strip():
        return "No content found in document."

    try:
        chunk = text.strip().replace("\n", " ")[:3000]
        summary = summarizer(chunk, max_length=150, min_length=50, do_sample=False)
        return summary[0]['summary_text']
    except Exception as e:
        return f"Failed to summarize: {e}"
