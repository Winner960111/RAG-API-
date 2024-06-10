from flask import Flask
from PDF_injest import pdf_embedding
from json_injest import json_embedding
from json_injest_mask import json_embedding_mask
from PDF_injest_mask import pdf_embedding_mask
from TXT_injest_mask import txt_embedding_mask
from TXT_injest import txt_embedding
from Delete_one import delete_db
from Delete_all import delete_db_all
from Query import query
from Query_unmask import query_unmask

app = Flask(__name__)

# PDF Injest (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/PDF_injest', methods = ['POST'])
def Create_PDF_Database():
    return pdf_embedding()

# PDF Injest w/ Masking (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/PDF_injest_mask', methods = ['POST'])
def Create_PDF_Database_mask():
    return pdf_embedding_mask()

# Text Injest (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/Text_injest', methods = ['POST'])
def Create_Text_Database():
    return txt_embedding()

# Text Injest w/ Masking(vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/Text_injest_mask', methods = ['POST'])
def Create_Text_Database_mask():
    return txt_embedding_mask()

# json Injest (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/json_injest', methods = ['POST'])
def Create_json_Database():
    return json_embedding()

# json Injest w/ Masking(vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/json_injest_mask', methods = ['POST'])
def Create_json_Database_mask():
    return json_embedding_mask()

# Query (Vectordb, prompt, Model, Model params)
@app.route('/query_unmask', methods = ['POST'])
def run_query_unmask():
    return query_unmask()

# Query with unmask (Vectordb, prompt, Model, Model params)
@app.route('/query', methods = ['POST'])
def run_query():
    return query()

# Delete special chroma DB (vectordb name)
@app.route('/delete_one_db', methods = ['DELETE'])
def delete_one_db():
    return delete_db()

# Delete all chroma DB (vectordb name)
@app.route('/delete_all_dbs', methods=['DELETE'])
def delete_all_dbs():
    return delete_db_all()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')