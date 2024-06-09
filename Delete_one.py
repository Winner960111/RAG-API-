from flask import request
from langchain_chroma import Chroma

def delete_db():
    db_name = request.form.get('vectordb_name')
    if not db_name:
        return "Input VectorDB name"
    ChromaDB = Chroma(persist_directory="./ChromaDB")

    ChromaDB._collection.delete(where={'vectordb_name':db_name})
    return "OK"