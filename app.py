import streamlit as st
from backend.utils import extract_text_from_file
from backend.summarizer import generate_summary
from backend.qna_engine import answer_question
from backend.challenge_me import generate_questions, evaluate_answers

st.set_page_config(page_title="DocuMentor | Smart Research Assistant")
st.title("📚 DocuMentor")
st.caption("An AI-powered assistant that reads, reasons, and challenges your understanding of any document.")

if "doc_text" not in st.session_state:
    st.session_state.doc_text = ""

uploaded_file = st.file_uploader("Upload your PDF or TXT document", type=["pdf", "txt"])

if uploaded_file:
    with st.spinner("Processing document..."):
        st.session_state.doc_text = extract_text_from_file(uploaded_file)

    st.success("Document uploaded and ready!")

    with st.expander("🔍 Auto Summary", expanded=True):
        summary = generate_summary(st.session_state.doc_text)
        st.markdown(summary)

    interaction_mode = st.radio("What would you like to do?", ["Ask Anything", "Challenge Me"], horizontal=True)

    if interaction_mode == "Ask Anything":
        st.subheader("💬 Ask Anything")
        user_question = st.text_input("Type your question based on the uploaded document:")
        if user_question:
            answer, reference = answer_question(st.session_state.doc_text, user_question)
            st.markdown(f"**Answer:** {answer}")
            st.markdown(f"📎 Reference: _{reference}_")

    elif interaction_mode == "Challenge Me":
        st.subheader("🧠 Challenge Me")

        if "questions" not in st.session_state:
            st.session_state.questions = generate_questions(st.session_state.doc_text)
            st.session_state.user_answers = ["" for _ in range(3)]

        for idx, question in enumerate(st.session_state.questions):
            st.text(f"Q{idx + 1}: {question}")
            st.session_state.user_answers[idx] = st.text_input(f"Your Answer {idx + 1}", key=f"ans_{idx}")

        if st.button("Submit Answers"):
            evaluation = evaluate_answers(
                st.session_state.doc_text,
                st.session_state.questions,
                st.session_state.user_answers
            )
            st.write("\n---")
            for i, feedback in enumerate(evaluation):
                st.markdown(f"**Q{i + 1} Evaluation:** {feedback['result']}")
                st.markdown(f"📝 Justification: _{feedback['justification']}_")
