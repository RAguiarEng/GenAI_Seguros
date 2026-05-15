import sys
import os
from pathlib import Path

# Adiciona a raiz do projeto no path para encontrar o 'src'
sys.path.append(str(Path(__file__).resolve().parent.parent))

from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever

def diagnostico():
    print("="*50)
    print("🔍 INICIANDO DIAGNÓSTICO DO RAG")
    print("="*50)
    
    print(f"\n1. Verificando pasta do banco de dados: {VECTOR_STORE_DIR}")
    if not os.path.exists(VECTOR_STORE_DIR):
        print("❌ ERRO: A pasta do banco de dados não existe!")
        return
    else:
        arquivos = os.listdir(VECTOR_STORE_DIR)
        print(f"✅ Pasta encontrada. Contém {len(arquivos)} arquivos/pastas.")
        
    print("\n2. Carregando o Retriever (ChromaDB)...")
    retriever = load_retriever(VECTOR_STORE_DIR)
    
    if not retriever:
        print("❌ ERRO: O load_retriever retornou None. O banco está vazio ou corrompido.")
        return
    print("✅ Retriever carregado com sucesso.")
    
    pergunta_teste = "Quais são as coberturas básicas do seguro Vida Flex?"
    print(f"\n3. Fazendo uma busca direta no banco de dados...")
    print(f"Pergunta: '{pergunta_teste}'")
    
    try:
        docs = retriever.invoke(pergunta_teste)
        print(f"\n✅ RESULTADO DA BUSCA: {len(docs)} documentos encontrados.")
        if len(docs) > 0:
            print("-" * 50)
            print("📜 PRIMEIRO DOCUMENTO ENCONTRADO:")
            print(docs[0].page_content[:300] + "...\n")
        else:
            print("❌ ALERTA: O Retriever funcionou, mas não encontrou NENHUM documento!")
    except Exception as e:
        print(f"❌ ERRO GRAVE DURANTE A BUSCA: {e}")

if __name__ == "__main__":
    diagnostico()
