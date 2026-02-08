from fastapi import FastAPI
from pydantic import BaseModel

from pipelines.ask_pipeline import ask
from pipelines.ask_image_pipeline import ask_image
from pipelines.sql_pipeline import run_sql_pipeline
from dotenv import load_dotenv
load_dotenv()

app = FastAPI(title="Enterprise RAG System")
@app.get("/")
def root():
    return {"status": "Enterprise RAG system running"}



class AskRequest(BaseModel):
    question: str
    context: str


class AskImageRequest(BaseModel):
    image_path: str
    question: str


class AskSQLRequest(BaseModel):
    question: str


@app.post("/ask")
def ask_text(req: AskRequest):
    """
    Text → Answer (RAG)
    """
    return ask(req.question, req.context)


@app.post("/ask-image")
def ask_image_endpoint(req: AskImageRequest):
    """
    Image → Text Answer
    """
    return ask_image(
        image_path=req.image_path,
        question=req.question
    )


@app.post("/ask-sql")
def ask_sql(req: AskSQLRequest):
    """
    Text → SQL → Answer
    """
    return run_sql_pipeline(req.question)
