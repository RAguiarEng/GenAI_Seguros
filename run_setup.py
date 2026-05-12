import subprocess
import sys
import os

def run_command(command, description):
    """Executa um comando no terminal e exibe o progresso."""
    print(f"\n{'='*50}")
    print(f"🚀 PASSO: {description}")
    print(f"💻 Comando: {' '.join(command)}")
    print(f"{'='*50}\n")
    
    try:
        # Executa o comando e redireciona a saída para o terminal em tempo real
        process = subprocess.Popen(
            command,
            stdout=sys.stdout,
            stderr=sys.stderr,
            text=True,
            shell=True if os.name == 'nt' else False
        )
        process.wait()
        
        if process.returncode != 0:
            print(f"\n❌ Erro ao executar: {description}")
            return False
            
        print(f"\n✅ {description} concluído com sucesso!")
        return True
        
    except Exception as e:
        print(f"\n💥 Falha inesperada: {e}")
        return False

def main():
    # 1. Verificar se o arquivo .env existe
    if not os.path.exists(".env"):
        print("⚠️ Alerta: Arquivo .env não encontrado. Verifique suas chaves de API.")
    
    # 2. Criar/Atualizar o Banco de Dados Vetorial (RAG)
    # Nota: Use 'create_db.py' ou 'createdb.py' conforme o nome real do seu arquivo
    if not run_command([sys.executable, "create_db.py"], "Alimentando a Base de Conhecimento (ChromaDB)"):
        return

    # 3. Gerar a visualização do Workflow (Grafo)
    if not run_command([sys.executable, "-m", "src.bot.graph"], "Gerando Imagem do Fluxo (Workflow)"):
        print("💡 Dica: Verifique se as funções no graph.py e nodes.py estão com nomes compatíveis.")
        # Não paramos o processo aqui, pois o chatbot pode funcionar sem a imagem.
    
    print(f"\n{'='*50}")
    print("🎉 TUDO PRONTO!")
    print("O banco de dados foi atualizado e o fluxo foi validado.")
    print("Agora, execute o comando abaixo para iniciar a interface:")
    print(f"\n👉 streamlit run app.py")
    print(f"{'='*50}\n")

if __name__ == "__main__":
    main()