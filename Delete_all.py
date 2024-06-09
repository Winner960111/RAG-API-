from flask import request
from langchain_chroma import Chroma

def delete_db_all():
   
    ChromaDB = Chroma(persist_directory="./ChromaDB")

    ChromaDB._collection.delete
    return "OK"