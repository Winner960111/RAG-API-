from flask import Flask, request, jsonify
from PDF_injest import pdf_embedding
from TXT_injest import txt_embedding
import os, shutil
# from PDF_masking import pdf_masking

app = Flask(__name__)

# PDF Injest (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/PDF_injest', methods = ['POST'])
def Create_PDF_Database():
    return pdf_embedding()

# Text Injest (vectordb name, namespace, ChunkMethod, Embed Method)
@app.route('/Text_injest', methods = ['POST'])
def Create_Text_Database():
    return txt_embedding()

# # PDF Injest w/ Masking (vectordb name, namespace, ChunkMethod, Embed Method)
# @app.route('/PDF_injest_mask', methods = ['POST'])
# def PDF_masking():
#     return pdf_masking()

# Delete special chroma DB (vectordb name)
@app.route('/delete_one_db', methods = ['DELETE'])
def delete_one_db():
    if request.method == 'DELETE':

        db_name = request.form.get('vectordb_name')
        db_path = f'./Databases/{db_name}'
        if os.path.exists(db_path):
            shutil.rmtree(db_path)  # Delete the directory containing the Chroma DB
            return jsonify({'message': f'{db_name} deleted successfully'})
        else:
            return jsonify({'message': f'{db_name} not found'})

    return 'OK'

# Delete special chroma DB (vectordb name)
@app.route('/delete_all_dbs', methods=['DELETE'])
def delete_all_dbs():
    if request.method == 'DELETE':
        db_path = './Databases'
        if os.path.exists(db_path):
            shutil.rmtree(db_path)  # Delete the directory containing all Chroma DBs
            os.makedirs(db_path)  # Recreate the empty directory
            return jsonify({'message': 'All DBs deleted successfully'})
        else:
            return jsonify({'message': 'No DBs found'})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')