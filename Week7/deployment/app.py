from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv

from src.pipelines.ask_pipeline import ask
from src.pipelines.ask_image_pipeline import ask_image
from src.pipelines.sql_pipeline import run_sql_pipeline

load_dotenv()

app = FastAPI(title="Enterprise RAG System")


@app.get("/")
def root():
    return {"status": "Enterprise RAG system running"}


# ---------- REQUEST MODELS ----------

class AskRequest(BaseModel):
    question: str


class AskImageRequest(BaseModel):
    question: str


class AskSQLRequest(BaseModel):
    question: str


# ---------- ENDPOINTS ----------

@app.post("/ask")
def ask_text(req: AskRequest):
    """
    Text → RAG Retrieval → Answer
    """
    return ask(req.question)


@app.post("/ask-image")
def ask_image_endpoint(req: AskImageRequest):
    """
    Image RAG (Search by question internally)
    """
    return ask_image(req.question)


@app.post("/ask-sql")
def ask_sql(req: AskSQLRequest):
    """
    SQL → Generate → Validate → Execute
    """
    return run_sql_pipeline(req.question)
