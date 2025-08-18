from transformers import pipeline
import random

qa_pipeline = pipeline("question-answering")

def generate_questions(document_text, num_questions=3):
    lines = [l.strip() for l in document_text.split(". ") if len(l.strip()) > 30]
    sampled = random.sample(lines, min(len(lines), num_questions))
    questions = [f"What is meant by: '{line[:50]}...'?" for line in sampled]
    return questions

def evaluate_answers(document_text, questions, user_answers):
    feedback_list = []
    for i in range(len(questions)):
        try:
            result = qa_pipeline(question=questions[i], context=document_text)
            expected = result['answer'].strip().lower()
            actual = user_answers[i].strip().lower()

            is_correct = actual in expected or expected in actual
            verdict = "✅ Correct" if is_correct else f"❌ Incorrect (Expected: {expected})"

            feedback_list.append({
                "result": verdict,
                "justification": f"Refer to: '{result['context'][:100]}...'"
            })
        except Exception as e:
            feedback_list.append({
                "result": "Error evaluating answer",
                "justification": str(e)
            })
    return feedback_list
