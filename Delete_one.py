from flask import request
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def delete_db():
    db_name = request.form.get('vectordb_name')
    if not db_name:
        return "Input VectorDB name"
    model_name = ['roberta-base', 'all-MiniLM-L6-v2', 'squeezebert/squeezebert-uncased']
    for model in model_name:
        embedding_function = SentenceTransformerEmbeddings(model_name=model)
        ChromaDB = Chroma(persist_directory=f"./Databases/{model}", embedding_function=embedding_function)
        ChromaDB._collection.delete(where={'vectordb_name':db_name})
    return "OK"