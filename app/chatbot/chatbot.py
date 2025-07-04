# app/chatbot/chatbot.py

# app/chatbot/chatbot.py

from langchain.chains import RetrievalQA
from langchain_community.llms import Ollama
from app.chatbot.ingest_docs import load_vectorstore

def build_chatbot_chain():
    llm = Ollama(
        model="mistral",  # or "llama3" if mistral not available
        temperature=0
        # ⚠️ Remove stream=True to avoid Pydantic validation error
    )

    vectorstore = load_vectorstore()
    retriever = vectorstore.as_retriever(search_kwargs={"k": 2})  # smaller = faster
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=False
    )
    return qa_chain
