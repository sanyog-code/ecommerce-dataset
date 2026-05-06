RAG Project Structure:

ecomerce-dataset/

│

├── app.py              # Streamlit frontend

├── ingest.py           # Data ingestion + FAISS index creation

├── rag_pipeline.py     # RAG pipeline definition

├── main.py             # FastAPI backend

├── requirements.txt    # Python dependencies

├── Dockerfile          # Docker build file

├── README.md

└── .env

├── .github/

│   └── workflows/

│       └── ci-cd.yml   # GitHub Actions pipeline

└── data/

    ├── walmart-products.csv