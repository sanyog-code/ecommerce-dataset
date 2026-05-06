from fastapi import FastAPI, Query
from rag_pipeline import load_pipeline, ask_question

app = FastAPI(title="Walmart E-Commerce RAG API")

chain = load_pipeline()


@app.post("/chat")
def chat(query: str = Query(..., description="Customer query")):
    return ask_question(chain, query)