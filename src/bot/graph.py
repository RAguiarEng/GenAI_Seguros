from langgraph.graph import StateGraph, END
from src.bot.state import AgentState
from src.bot.nodes import get_analise_node, node_pedir_contexto, node_info_nao_encontrada, decidir_fluxo_pos_analise

def compile_agent(retriever):
    workflow = StateGraph(AgentState)
    
    workflow.add_node("analise_financeira", get_analise_node(retriever))
    workflow.add_node("pedir_contexto", node_pedir_contexto)
    workflow.add_node("info_nao_encontrada", node_info_nao_encontrada)
    
    workflow.set_entry_point("analise_financeira")
    workflow.add_conditional_edges(
        "analise_financeira",
        decidir_fluxo_pos_analise,
        {"pedir_contexto": "pedir_contexto", "info_nao_encontrada": "info_nao_encontrada", "fim": END}
    )
    workflow.add_edge("pedir_contexto", END)
    workflow.add_edge("info_nao_encontrada", END)
    
    return workflow.compile()