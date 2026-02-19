import streamlit as st

from pipelines.ask_pipeline import ask
from pipelines.ask_image_pipeline import ask_image
from pipelines.sql_pipeline import run_sql_pipeline
from dotenv import load_dotenv
load_dotenv()


st.set_page_config(page_title="Enterprise RAG System", layout="centered")

st.title("Enterprise RAG System")
st.caption("Text RAG • Image RAG • SQL QA")

mode = st.selectbox(
    "Choose Query Mode",
    ["Text (RAG)", "Image → Text (Image RAG)", "SQL Question Answering"]
)

if mode == "Text (RAG)":
    st.subheader("Text Question Answering")

    question = st.text_input("Enter your question")

    if st.button("Ask"):
        if question:
            result = ask(question)

            st.markdown("Answer")
            st.write(result["answer"])

            st.markdown("Evaluation")
            st.json(result["evaluation"])
        else:
            st.warning("Please enter a question.")



elif mode == "Image → Text (Image RAG)":
    st.subheader("Image Question Answering")

    question = st.text_input("Ask about images in documents")

    if st.button("Analyze"):
        if question:
            result = ask_image(question)

            st.markdown("Answer")
            st.write(result["answer"])

            st.markdown("Evaluation")
            st.json(result["evaluation"])

            st.markdown("Retrieved Images")
            for path in result["retrieved_images"]:
                st.image(path)
        else:
            st.warning("Enter a question.")



elif mode == "SQL Question Answering":
    st.subheader("SQL QA")

    question = st.text_input("Enter SQL question")

    if st.button("Run SQL"):
        if question:
            result = run_sql_pipeline(question)

            st.markdown("Generated SQL")
            st.code(result["sql"], language="sql")

            st.markdown("Result")
            st.json(result["result"])
        else:
            st.warning("Enter a question.")
