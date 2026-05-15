from langgraph.graph import StateGraph, END
from src.bot.state import AgentState
from src.bot.nodes import get_knowledge_retrieval_node, get_generation_node

def compile_agent(retriever):
    workflow = StateGraph(AgentState)
    
    # Adicionamos apenas os dois Atores necessários
    workflow.add_node("retrieve", get_knowledge_retrieval_node(retriever))
    workflow.add_node("generate", get_generation_node())
    
    # O Fluxo é linear: Começa na Busca -> Vai para a Geração -> Termina
    workflow.set_entry_point("retrieve")
    workflow.add_edge("retrieve", "generate")
    workflow.add_edge("generate", END)
    
    return workflow.compile()
