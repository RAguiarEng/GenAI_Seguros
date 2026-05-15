import time
import os
from langchain_chroma import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai.embeddings import GoogleGenerativeAIError
from tqdm.auto import tqdm
from src.config import GOOGLE_API_KEY, EMBEDDING_MODEL, SCORE_THRESHOLD, TOP_K

def get_embeddings():
    return GoogleGenerativeAIEmbeddings(
        model=EMBEDDING_MODEL,
        google_api_key=GOOGLE_API_KEY
    )

def create_vector_store(chunks, save_path):
    if not chunks:
        return None
        
    embeddings = get_embeddings()
    batch_size = 20
    
    # Inicializa o Chroma apontando para o diretório de persistência
    print(f"Inicializando ChromaDB em {save_path}...")
    vectorstore = Chroma(
        collection_name="finance_docs",
        embedding_function=embeddings,
        persist_directory=str(save_path)
    )
    
    print(f"Processando e inserindo em lotes de {batch_size} chunks...")
    for i in tqdm(range(0, len(chunks), batch_size)):
        batch = chunks[i:i + batch_size]
        while True:
            try:
                # O Chroma salva no disco automaticamente a cada inserção na versão atual
                vectorstore.add_documents(batch)
                break
            except GoogleGenerativeAIError as e:
                if "429" in str(e):
                    print("\nCota de API atingida. Aguardando 61s...")
                    time.sleep(61)
                else:
                    raise e
                    
    print(f"\nVector Store (Chroma) populado e salvo com sucesso em: {save_path}")

def load_retriever(store_path):
    # Verifica se a pasta do Chroma existe e não está vazia
    if not os.path.exists(store_path) or not os.listdir(store_path):
        return None
    
    embeddings = get_embeddings()
    
    # Carrega a base persistida no disco
    vectorstore = Chroma(
        collection_name="finance_docs",
        embedding_function=embeddings,
        persist_directory=str(store_path)
    )
    
    return vectorstore.as_retriever(search_kwargs={"k": TOP_K}, search_type="similarity")