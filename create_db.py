from src.config import DATA_RAW_DIR, VECTOR_STORE_DIR
from src.data_ingestion.loader import load_and_split_documents
from src.rag.vector_store import create_vector_store

def main():
    print("Iniciando criação do banco de dados vetorial...")
    chunks = load_and_split_documents(DATA_RAW_DIR)
    
    if chunks:
        create_vector_store(chunks, VECTOR_STORE_DIR)
    else:
        print("Operação cancelada: Nenhum documento processado.")

if __name__ == "__main__":
    main()