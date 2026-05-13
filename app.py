import sys
from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

def main():
    print("Inicializando a aplicação...")
    
    # Carrega do disco a base de dados (Vector Store)
    retriever = load_retriever(VECTOR_STORE_DIR)
    
    if not retriever:
        print("ERRO: Vector Store não encontrado. Rode 'python create_db.py' primeiro.")
        return

    # Variável renomeada para inglês
    agent = compile_agent(retriever)
    print(">>> Agente pronto!\n")
    
    print("--- INICIANDO CHAT INTERATIVO (GENAI SEGUROS) ---")
    print("Para sair, digite 'sair', 'fim' ou 'exit'.")
    
    while True:
        try:
            user_input = input("\nVocê: ")
            if user_input.lower().strip() in ["sair", "fim", "exit"]:
                print("Encerrando a sessão...")
                sys.exit(0)

            if not user_input.strip():
                continue

            # Invocação usando a nova chave de estado 'question'
            state_response = agent.invoke({"question": user_input})
            
            # Extraindo a resposta usando a chave 'answer'
            print(f"\nAgente: {state_response.get('answer')}")
            
            # Extraindo as fontes usando a chave 'citations'
            citations = state_response.get("citations")
            if citations:
                print("\nFontes:")
                for c in citations:
                    # Chaves ajustadas para inglês
                    print(f" - {c.get('document', 'Desconhecido')} (Pág {c.get('page', 'N/A')}): {c.get('snippet', '')}")
            
            print("-" * 50)
            
        except KeyboardInterrupt:
            print("\nEncerrando...")
            break
        except Exception as e:
            print(f"\nOcorreu um erro: {e}")

if __name__ == "__main__":
    main()