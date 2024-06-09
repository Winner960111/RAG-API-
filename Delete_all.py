from flask import request
from langchain_chroma import Chroma
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)

def delete_db_all():
    model_name = ['roberta-base', 'all-MiniLM-L6-v2', 'squeezebert/squeezebert-uncased']
    for model in model_name:
        embedding_function = SentenceTransformerEmbeddings(model_name=model)
        ChromaDB = Chroma(persist_directory=f"./Databases/{model}", embedding_function=embedding_function)
        ChromaDB.delete_collection()
    return "OK"