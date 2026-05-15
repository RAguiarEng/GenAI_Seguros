import subprocess
import sys
import os
from pathlib import Path

# Executa um comando no terminal e exibe o progresso
def run_command(command_list, description):
    print(f"\n{'='*50}")
    print(f">>> PASSO: {description}")
    print(f">>> COMANDO: {' '.join(command_list)}")
    print(f"{'='*50}\n")
    
    try:
        # Executa o comando e redireciona a saída para o terminal em tempo real
        process = subprocess.Popen(
            command_list,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            shell=True if os.name == 'nt' else False
        )
        process.wait()
        
        if process.returncode != 0:
            print(f"\n>>> ERRO: Erro ao executar: {description}")
            return False
            
        print(f"\n>>> {description} concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n>>> ERRO: Falha inesperada: {e}")
        return False

def main():
    # 1. Verificar se o arquivo .env existe
    if not os.path.exists(".env"):
        print(">>> ALERTA: Arquivo .env não encontrado. Verifique suas chaves de API.")
    
    # 2. Criar/Atualizar o Banco de Dados Vetorial (RAG)
    
    vector_store_path = Path("data/vector_store") # Define o caminho onde o ChromaDB salva os arquivos
    
    # Verifica se a pasta existe e se não está vazia
    if vector_store_path.exists() and any(vector_store_path.iterdir()):
        print(f"\n{'='*50}")
        print(">>> PASSO IGNORADO: Alimentando a Base de Conhecimento (ChromaDB)")
        print(">>> Motivo: O banco de dados vetorial já existe na pasta 'data/vector_store/'.")
        print(">>> Para recriá-lo, apague a pasta manualmente e rode este script novamente.")
        print(f"{'='*50}\n")
    else:
        # Só roda o create_db.py se a pasta não existir ou estiver vazia
        if not run_command([sys.executable, "create_db.py"], "Alimentando a Base de Conhecimento (ChromaDB)"):
            return

    # 3. Gerar a visualização do Workflow (Grafo)
    if not run_command([sys.executable, "-m", "src.bot.graph"], "Gerando Imagem do Fluxo (Workflow)"):
        print(">>> DICA: Verifique se as funções no graph.py e nodes.py estão com nomes compatíveis.")
    
    print(f"\n{'='*50}")
    print(">>> SETUP FINALIZADO COM SUCESSO!")
    print("Agora você pode rodar 'streamlit run teste.py' ou 'python app.py'")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()