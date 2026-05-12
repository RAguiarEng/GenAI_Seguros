from langgraph.graph import StateGraph, END
from src.bot.state import AgentState

# Aqui usamos os nomes exatos que estão no arquivo nodes.py
from src.bot.nodes import (
    get_analise_node, 
    node_pedir_contexto, 
    node_info_nao_encontrada, 
    decidir_fluxo_pos_analise
)

def compile_agent(retriever):
    """
    Compila o fluxo de conversação do LangGraph para o chatbot da GenAI Seguros.
    """
    # Inicializa o grafo com o estado do agente
    workflow = StateGraph(AgentState)
    
    # Mapeamento dos nós do fluxo:
    workflow.add_node("analise_duvida_seguro", get_analise_node(retriever))
    workflow.add_node("pedir_contexto_seguro", node_pedir_contexto)
    workflow.add_node("info_nao_encontrada", node_info_nao_encontrada)
    
    # Define onde a conversa começa
    workflow.set_entry_point("analise_duvida_seguro")
    
    # Lógica de Roteamento Condicional
    workflow.add_conditional_edges(
        "analise_duvida_seguro",
        decidir_fluxo_pos_analise,
        {
            "pedir_contexto": "pedir_contexto_seguro",
            "info_nao_encontrada": "info_nao_encontrada",
            "fim": END
        }
    )
    
    # Definindo os pontos finais do fluxo
    workflow.add_edge("pedir_contexto_seguro", END)
    workflow.add_edge("info_nao_encontrada", END)
    
    # Compila a aplicação
    return workflow.compile()

# --- CÓDIGO PARA GERAR O GRAFO ---
if __name__ == "__main__":
    print("Gerando visualização do fluxo...")
    
    # Compilamos com None apenas para visualização da estrutura
    app_visualizacao = compile_agent(retriever=None)
    
    try:
        # Tenta gerar a imagem PNG
        imagem_png = app_visualizacao.get_graph().draw_mermaid_png()
        with open("docs/fluxo_genai_seguros.png", "wb") as f:
            f.write(imagem_png)
        print("✅ Sucesso! Imagem salva como 'docs/fluxo_genai_seguros.png'.")
    except Exception as e:
        print(f"⚠️ Erro ao gerar PNG: {e}")
        print("\nExibindo versão ASCII:\n")
        print(app_visualizacao.get_graph().draw_ascii())