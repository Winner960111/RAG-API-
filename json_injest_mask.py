from flask import request
from langchain_chroma import Chroma
from langchain_community.document_loaders import JSONLoader
from langchain_text_splitters import CharacterTextSplitter
from langchain_community.embeddings.sentence_transformer import (
    SentenceTransformerEmbeddings,
)
import os, re, spacy, uuid, sqlite3

# Load the English language model
nlp = spacy.load('en_core_web_sm')

def extract_names(text):
    doc = nlp(text)
    names = []
    for ent in doc.ents:
        if ent.label_ == 'PERSON':
            if not re.findall('@', ent.text):
                names.append(ent.text)
    return names

def json_embedding_mask():
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
        # Create the sqliteDB if it isn't exist
        if (os.path.isfile(f'./sqliteDB/Database.db') == False):
            con = sqlite3.connect(f'./sqliteDB/Database.db')
            cur = con.cursor()
            cur.execute("CREATE TABLE uuid_info(vectordb_name, namespace, style, real, uuid)")
            con.close()

        ## file contents load
        # List all files in the special directory
        files_in_directory = os.listdir(Uploaded_dir)
        for file_name in files_in_directory:

            try:
                loader = JSONLoader(rf"{Uploaded_dir}/{file_name}")
            except:
                return "Invalid file format"
            
            documents= loader.load()
        
            # split it into chunks
            text_splitter = CharacterTextSplitter(chunk_size=int(chunk_size), chunk_overlap=int(chunk_overlap))
            docs = text_splitter.split_documents(documents)
            for index in range(0, len(docs)):
                docs[index].metadata['namespace'] = namespace
                docs[index].metadata['vectordb_name'] = vectordb_name

                # Mask functionality
                name = extract_names(docs[index].page_content)
                email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', docs[index].page_content)
                credit_card = re.findall(r'\b\d{16}\b', docs[index].page_content)
                phone_number = re.findall(r'\b\d{3}-\d{3}-\d{4}\b', docs[index].page_content)
                print(f"\n\nthis is name===>{name}, {email}, {credit_card}, {phone_number}")

                # Connect to the SQLite database
                conn = sqlite3.connect(f'./sqliteDB/Database.db')  # Replace 'database.db' with your database file

                # Create a cursor object to execute SQL queries
                cursor = conn.cursor()
                # create UUID letters
                for item in name:
                    uuid_str = str(uuid.uuid4())

                    # Insert data into a specific table
                    cursor.execute("INSERT INTO uuid_info (vectordb_name, namespace, style, real, uuid) VALUES (?, ?, ?, ?, ?)", (vectordb_name, namespace, 'name', item, uuid_str))

                    # Commit the changes to the database
                    conn.commit()
                    
                    docs[index].page_content = re.sub(item, uuid_str, docs[index].page_content)

                for item in phone_number:
                    uuid_str = str(uuid.uuid4())

                    # Insert data into a specific table
                    cursor.execute("INSERT INTO uuid_info (vectordb_name, namespace, style, real, uuid) VALUES (?, ?, ?, ?, ?)", (vectordb_name, namespace, 'phone_number', item, uuid_str))

                    # Commit the changes to the database
                    conn.commit()
                    
                    docs[index].page_content = re.sub(item, uuid_str, docs[index].page_content)
                
                for item in credit_card:
                    uuid_str = str(uuid.uuid4())

                    # Insert data into a specific table
                    cursor.execute("INSERT INTO uuid_info (vectordb_name, namespace, style, real, uuid) VALUES (?, ?, ?, ?, ?)", (vectordb_name, namespace, 'credit_card', item, uuid_str))
                    # Commit the changes to the database
                    conn.commit()
                    
                    docs[index].page_content = re.sub(item, uuid_str, docs[index].page_content)
                
                for item in email:
                    uuid_str = str(uuid.uuid4())

                    # Insert data into a specific table
                    cursor.execute("INSERT INTO uuid_info (vectordb_name, namespace, style, real, uuid) VALUES (?, ?, ?, ?, ?)", (vectordb_name, namespace, 'eamil', item, uuid_str))

                    # Commit the changes to the database
                    conn.commit()
                    
                    docs[index].page_content = re.sub(item, uuid_str, docs[index].page_content)

                # Close the connection
                conn.close()

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