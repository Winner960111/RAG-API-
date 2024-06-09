from flask import request
from langchain_chroma import Chroma
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import os

def pdf_embedding():
    if request.method == 'POST':
        Uploaded_files = request.files.getlist('files')
        
        # Check if any file has been uploaded
        files_uploaded = any(file.filename for file in Uploaded_files)
        
        if not files_uploaded:
            return "Upload source files."
        
        # Get essential information from request.
        vectordb_name = request.form.get('Vectordb_name')
        if not vectordb_name:
            return 'Input Vectordb name'
        
        namespace = request.form.get('Namespace')
        if not namespace:
            return 'Input namespace'
        
        chunk_size = request.form.get('Chunk_size')
        if not chunk_size:
            return 'Input chunk size'
        
        chunk_overlap = request.form.get('Chunk_overlap')
        if not chunk_overlap:
            return 'Input chunk overlap'
        
        embed_method = request.form.get('Embed_method')
        if not embed_method:
            return 'Input embed method'

        # format the directory
        # Specify the path to the special directory where files are located
        Uploaded_dir = './Uploaded_files'

        # List all files in the special directory
        files_in_directory = os.listdir(Uploaded_dir)

        # Iterate over each file in the directory and delete them
        for file_name in files_in_directory:
            file_path = os.path.join(Uploaded_dir, file_name)
            os.remove(file_path)

        # save files in local
        for file in Uploaded_files:
            file.save(os.path.join(Uploaded_dir, file.filename))

        ## file contents load
        # List all files in the special directory
        files_in_directory = os.listdir(Uploaded_dir)
        for file_name in files_in_directory:
            
            loader = PyPDFLoader(rf"{Uploaded_dir}/{file_name}")
            documents= loader.load()
        
            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=int(chunk_size), chunk_overlap=int(chunk_overlap))
            docs = text_splitter.split_documents(documents)
            for index in range(0, len(docs)):
                docs[index].metadata['namespace'] = namespace
                docs[index].metadata['vectordb_name'] = vectordb_name
            
            # Choose embed method
            match embed_method:

                case "improved_language_understanding":
                    model = "roberta-base"
                
                case "wide_range_NLP":
                    model = "all-MiniLM-L6-v2"

                case "resource_constrained_env":
                    model = "squeezebert/squeezebert-uncased"

                case _:
                    model = "None"
                    
            if model == "None":
                return "Input correct model name"
            # create the open-source embedding function
            embedding_function = SentenceTransformerEmbeddings(model_name=model)
            
            # load it into Chroma
            Chroma.from_documents(docs, embedding_function, persist_directory=f"./Databases/{model}")

    return 'OK'