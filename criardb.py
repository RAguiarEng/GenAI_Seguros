import os
import shutil
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_chroma import Chroma
from dotenv import load_dotenv

load_dotenv()

def create_db():
    caminho_db = "db"
    
    # Carregar documentos da pasta /data
    print("Carregando PDFs da pasta /data...")
    loader = PyPDFDirectoryLoader("data")
    documentos = loader.load()
    
    # Dividir em chunks para otimizar o limite de tokens
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=2000,
        chunk_overlap=500,
        length_function=len
    )
    chunks = text_splitter.split_documents(documentos)
    
    # Limpar banco antigo se existir
    if os.path.exists(caminho_db):
        shutil.rmtree(caminho_db)
        
    # Vetorizar os chunks e salvar localmente usando o Chroma
    print("Vetorizando dados...")
    funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma.from_documents(chunks, funcao_embedding, persist_directory=caminho_db)
    
    print(f"Banco vetorizado criado com sucesso! Total de chunks: {len(chunks)}")

if __name__ == "__main__":
    create_db()