# list_models.py
import os
from dotenv import load_dotenv
from google import genai

# Carrega o arquivo .env da raiz do projeto (mesma pasta onde está seu create_db.py, por exemplo)
load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("Variável de ambiente GOOGLE_API_KEY não definida.")

client = genai.Client(api_key=api_key)

def main():
    print("Listando modelos disponíveis...\n")
    models = client.models.list()
    for m in models:
        name = getattr(m, "name", None) or getattr(m, "model", "sem_nome")
        supported = getattr(m, "supported_generation_methods", [])
        print(f"Modelo: {name}")
        print(f"  Métodos suportados: {supported}")
        print("-" * 60)

if __name__ == "__main__":
    main()