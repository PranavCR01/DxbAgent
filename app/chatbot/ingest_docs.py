# app/chatbot/ingest_docs.py


# app/chatbot/ingest_docs.py

import os
from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

PDF_DIR = "data"
VECTOR_DB_PATH = "data/faq_faiss_index"

def ingest_local_pdfs():
    pdf_files = [f for f in os.listdir(PDF_DIR) if f.endswith(".pdf")]
    docs = []

    for filename in pdf_files:
        path = os.path.join(PDF_DIR, filename)
        loader = PyPDFLoader(file_path=path)
        docs.extend(loader.load())

    print(f"✅ Loaded {len(pdf_files)} PDFs, split into {len(docs)} chunks.")

    splitter = RecursiveCharacterTextSplitter(chunk_size=800, chunk_overlap=100)
    chunks = splitter.split_documents(docs)

    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    vectordb = FAISS.from_documents(chunks, embedder)
    vectordb.save_local(VECTOR_DB_PATH)
    print("✅ Vector DB saved at:", VECTOR_DB_PATH)

def load_vectorstore():
    embedder = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    try:
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings=embedder,
            allow_dangerous_deserialization=True  # required to load from .pkl
        )
    except Exception as e:
        print(f"⚠️ Failed to load FAISS index: {e}. Ingesting from scratch.")
        ingest_local_pdfs()
        return FAISS.load_local(
            VECTOR_DB_PATH,
            embeddings=embedder,
            allow_dangerous_deserialization=True
        )
