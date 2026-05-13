from langgraph.graph import StateGraph, END
from src.bot.state import AgentState

# Aqui usamos os nomes exatos que estão no arquivo nodes.py
from src.bot.nodes import (
    intent_routing_node,
    get_knowledge_retrieval_node,
    answer_check_node,
    ask_context_node,
    human_handoff_node,
    route_after_intent,
    route_after_check
)

# Compila o fluxo de conversação (Flow Engineering) 
def compile_agent(retriever):
    workflow = StateGraph(AgentState)
    
    # Adicionando os nodes (Atores do sistema)
    workflow.add_node("intent_routing", intent_routing_node)
    workflow.add_node("knowledge_retrieval", get_knowledge_retrieval_node(retriever))
    workflow.add_node("answer_check", answer_check_node)
    workflow.add_node("ask_context", ask_context_node)
    workflow.add_node("human_handoff", human_handoff_node)
    
    # Ponto de Entrada
    workflow.set_entry_point("intent_routing")
    
    # Caminhos Condicionais (Intenção -> RAG ou Humano)
    workflow.add_conditional_edges(
        "intent_routing",
        route_after_intent,
        {
            "knowledge_retrieval": "knowledge_retrieval",
            "human_handoff": "human_handoff"
        }
    )
    
    # O node de busca RAG sempre avança para a verificação de alucinação
    workflow.add_edge("knowledge_retrieval", "answer_check")
    
    # Caminhos Condicionais Pós-RAG (Confiança da Resposta vs. Ambiguidade)
    workflow.add_conditional_edges(
        "answer_check",
        route_after_check,
        {
            "end": END,
            "ask_context": "ask_context",
            "human_handoff": "human_handoff"
        }
    )
    
    # Encerrando os nodes sem saída
    workflow.add_edge("ask_context", END)
    workflow.add_edge("human_handoff", END)
    
    return workflow.compile()

# Visualização do fluxo (Grafo)
if __name__ == "__main__":
    print("Gerando visualização do fluxo do LangGraph...")
    app_view = compile_agent(retriever=None)
    
    try:
        png_image = app_view.get_graph().draw_mermaid_png()
        with open("docs/fluxo_genai_seguros.png", "wb") as f:
            f.write(png_image)
        print("Sucesso! Imagem salva como 'docs/fluxo_genai_seguros.png'.")
    except Exception as e:
        print(f"Erro ao gerar PNG: {e}")