from flask import Flask, request, jsonify
from PDF_injest import pdf_embedding
from PDF_injest_mask import pdf_embedding_mask
from TXT_injest_mask import txt_embedding_mask
from TXT_injest import txt_embedding
from Query import query
import os, shutil

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

# Query (Vectordb, prompt, Model, Model params)
@app.route('/query', methods = ['POST'])
def run_query():
    return query()

# Delete special chroma DB (vectordb name)
@app.route('/delete_one_db', methods = ['DELETE'])
def delete_one_db():
    try:

        if request.method == 'DELETE':

            db_name = request.form.get('vectordb_name')
            db_path = f'./Databases/{db_name}'
            if os.path.exists(db_path):
                shutil.rmtree(db_path)  # Delete the directory containing the Chroma DB
                return jsonify({'message': f'{db_name} deleted successfully'})
            else:
                return jsonify({'message': f'{db_name} not found'})
    except Exception as e:
        print(e)
        return jsonify({'error': e})

# Delete special chroma DB (vectordb name)
@app.route('/delete_all_dbs', methods=['DELETE'])
def delete_all_dbs():
    try:

        if request.method == 'DELETE':
            db_path = './Databases'
            if os.path.exists(db_path):
                shutil.rmtree(db_path)  # Delete the directory containing all Chroma DBs
                os.makedirs(db_path)  # Recreate the empty directory
                return jsonify({'message': 'All DBs deleted successfully'})
            else:
                return jsonify({'message': 'No DBs found'})
    except Exception as e:
        print(e)
        return jsonify({'error': e})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')