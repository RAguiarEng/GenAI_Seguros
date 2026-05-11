from src.bot.state import AgentState
from src.rag.chain import get_rag_chain, formatar_citacoes

KEYWORDS_AMBIGUAS = ["fale sobre", "resuma", "visão geral", "como está"]

def get_analise_node(retriever):
    chain = get_rag_chain()
    
    def node_analise_financeira(state: AgentState) -> AgentState:
        if not retriever:
            return {"resposta": "Nenhum documento carregado.", "citacoes": [], "contexto_encontrado": False}
            
        docs_relacionados = retriever.invoke(state["pergunta"])
        if not docs_relacionados:
            return {"resposta": "Não consta no documento fornecido.", "citacoes": [], "contexto_encontrado": False}
            
        response = chain.invoke({"input": state["pergunta"], "context": docs_relacionados})
        txt = (response or "").strip()
        
        if txt == "Não consta no documento fornecido.":
            return {"resposta": txt, "citacoes": [], "contexto_encontrado": False}
            
        return {
            "resposta": txt,
            "citacoes": formatar_citacoes(docs_relacionados, state["pergunta"]),
            "contexto_encontrado": True
        }
    return node_analise_financeira

def node_pedir_contexto(state: AgentState) -> AgentState:
    return {
        "resposta": "Sua pergunta parece ambígua. Por favor, forneça mais contexto.",
        "citacoes": [],
        "acao_final": "PEDIR_CONTEXTO"
    }

def node_info_nao_encontrada(state: AgentState) -> AgentState:
    return {
        "resposta": "Não consta no documento fornecido.",
        "citacoes": [],
        "acao_final": "INFO_NAO_ENCONTRADA"
    }

def decidir_fluxo_pos_analise(state: AgentState) -> str:
    if state.get("contexto_encontrado"):
        state["acao_final"] = "ANALISE_CONCLUIDA"
        return "fim"
    if any(keyword in state["pergunta"].lower() for keyword in KEYWORDS_AMBIGUAS):
        return "pedir_contexto"
    return "info_nao_encontrada"