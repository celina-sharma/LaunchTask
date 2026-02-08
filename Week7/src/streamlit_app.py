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
    context = st.text_area("Context (retrieved text / docs)")

    if st.button("Ask"):
        if question and context:
            result = ask(question, context)

            st.markdown("Answer")
            st.write(result["answer"])

            st.markdown("Evaluation")
            st.json(result["evaluation"])
        else:
            st.warning("Please provide both question and context.")

elif mode == "Image → Text (Image RAG)":
    st.subheader("Image Understanding")

    image_path = st.text_input("Image path")
    question = st.text_input("Question about the image")

    if image_path:
        try:
            st.image(image_path, caption="Input Image", use_column_width=True)
        except:
            st.warning("Unable to display image. Check path.")

    if st.button("Analyze Image"):
        if image_path and question:
            result = ask_image(image_path, question)

            st.markdown("Answer")
            st.write(result["answer"])

            st.markdown("Evaluation")
            st.json(result["evaluation"])
        else:
            st.warning("Please provide image path and question.")

elif mode == "SQL Question Answering":
    st.subheader("SQL Question Answering")

    question = st.text_input("Enter SQL question")

    if st.button("Run SQL"):
        if question:
            result = run_sql_pipeline(question)

            st.markdown("Generated SQL")
            st.code(result["sql"], language="sql")

            st.markdown("Result")
            st.json(result["result"])
        else:
            st.warning("Please enter a question.")
