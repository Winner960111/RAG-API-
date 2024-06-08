from flask import request
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def delete_db():
    db_name = request.form.get('vectordb_name')
    if not db_name:
        return "Input VectorDB name"
    embedding_function = SentenceTransformerEmbeddings(model_name="all-MiniLM-L6-v2")
    ChromaDB = Chroma(persist_directory="./ChromaDB", embedding_function=embedding_function)

    ChromaDB._collection.delete(where={'vectordb_name':db_name})
    return "OK"