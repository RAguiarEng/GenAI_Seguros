from pathlib import Path
from langchain_community.document_loaders import PyMuPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.config import CHUNK_SIZE, CHUNK_OVERLAP

# Função para carregar documentos PDF de uma pasta, 
# dividir em chunks e retornar a lista de chunks
def load_and_split_documents(folder_path: str | Path):
    docs = []
    drive_folder = Path(folder_path)
    
    # Verifica se a pasta existe antes de tentar carregar os arquivos
    if not drive_folder.exists():
        print(f"ERRO: A pasta '{folder_path}' não foi encontrada.")
        return []
        
    pdf_files = list(drive_folder.glob("*.pdf"))
    
    for n in pdf_files:
        try:
            loader = PyMuPDFLoader(str(n))
            docs.extend(loader.load())
            print(f"Carregado: {n.name}")
        except Exception as e:
            print(f"Erro ao carregar {n.name}: {e}")
            
    # Configura o splitter para dividir os documentos em chunks menores
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=CHUNK_SIZE, 
        chunk_overlap=CHUNK_OVERLAP
    )
    # Divide os documentos em chunks e retorna a lista de chunks
    chunks = splitter.split_documents(docs)
    print(f"Total de chunks gerados: {len(chunks)}")
    return chunks