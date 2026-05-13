import os 
from pathlib import Path
from dotenv import load_dotenv

# Carrega variáveis de ambiente do arquivo .env
load_dotenv()

# Chaves e APIs
GOOGLE_API_KEY = os.environ.get("GOOGLE_API_KEY")

# Define o provedor de LLM com base na variável de ambiente, padrão para 'google'
LLM_PROVIDER = os.environ.get("LLM_PROVIDER", "google").lower()

# Diretórios
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_RAW_DIR = BASE_DIR / "data" / "raw"
VECTOR_STORE_DIR = BASE_DIR / "data" / "vector_store"

# Modelos
EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "models/gemini-embedding-001")
LLM_MODEL = os.environ.get("LLM_MODEL", "gemini-2.5-flash")

# Parâmetros RAG
CHUNK_SIZE = 1500
CHUNK_OVERLAP = 150
SCORE_THRESHOLD = 0.4
TOP_K = 5