import sys
from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

def main():
    print("Inicializando a aplicação...")
    
    # Carrega do disco em vez de processar PDFs na hora
    retriever = load_retriever(VECTOR_STORE_DIR)
    
    if not retriever:
        print("ERRO: Vector Store não encontrado. Rode 'python createdb.py' primeiro.")
        return

    agente_financeiro = compile_agent(retriever)
    print("Agente pronto!\n")
    
    print("--- INICIANDO CHAT INTERATIVO ---")
    print("Para sair, digite 'sair', 'fim' ou 'exit'.")
    
    while True:
        try:
            pergunta = input("\nVocê: ")
            if pergunta.lower().strip() in ["sair", "fim", "exit"]:
                print("Encerrando a sessão...")
                sys.exit(0)

            resposta = agente_financeiro.invoke({"pergunta": pergunta})
            print(f"\nAgente: {resposta.get('resposta')}")
            
            citacoes = resposta.get("citacoes")
            if citacoes:
                print("\nFontes:")
                for c in citacoes:
                    print(f" - {c['documento']} (Pág {c['pagina']}): {c['trecho']}")
            
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            sys.exit(0)
        except Exception as e:
            print(f"Erro: {e}")

if __name__ == "__main__":
    main()