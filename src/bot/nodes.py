from src.bot.state import AgentState
from src.rag.chain import get_rag_chain, format_citations

# Palavras-chave que indicam pedidos muito amplos ou genéricos
AMBIGUOUS_KEYWORDS = [
    "fale sobre", "resuma", "visão geral", "como está", "acionar", "o que é", 
    "explique", "detalhes", "diga mais", "conte mais", "quais são", "quais as", 
    "quais os", "quais informações", "quais dados"
]

# Classifica a intenção da dúvida do cliente (Sinistro, FAQ, Financeiro).
def intent_routing_node(state: AgentState) -> str:
    question = state.get("question", "").lower()
    
    if any(word in question for word in ["sinistro", "bater", "roubar", "acidente", "guincho"]):
        intent = "SINISTRO"
    elif any(word in question for word in ["pagamento", "boleto", "fatura", "financeiro"]):
        intent = "FINANCEIRO"
    else:
        intent = "FAQ"
        
    return {"intent": intent}

# Busca semântica nos manuais da seguradora via RAG
def get_knowledge_retrieval_node(retriever):
    chain = get_rag_chain()

    def knowledge_retrieval_node(state: AgentState) -> AgentState:
        question = state.get("question", "")
        docs = retriever.invoke(question)
        
        # Se os PDFs não falarem sobre o assunto
        if not docs:
            return {
                "answer": "Sinto muito, mas não encontrei essa informação específica nos manuais disponíveis. Por favor, consulte seu corretor ou o portal oficial para detalhes adicionais.",
                "citations": [],
                "context_found": False
            }
            
        # formatted_context = "\n\n".join([doc.page_content for doc in docs])
        
        answer = chain.invoke({
            "question": question,
            "context": docs,
            "docs": docs
        })
        
        return {
            "answer": answer,
            "citations": format_citations(docs, question),
            "context_found": True
        }
    return knowledge_retrieval_node

# Alucinações podem ocorrer quando o modelo tenta responder sem ter contexto suficiente ou quando a pergunta é muito genérica. 
# Este node avalia a resposta gerada e define um nível de confiança, que será usado para decidir o próximo passo do fluxo (responder, pedir mais contexto ou transferir para humano).
def answer_check_node(state: AgentState) -> AgentState:
    answer = state.get("answer", "")
    context_found = state.get("context_found", False)
    
    confidence = True
    # Perde a confiança se o RAG falhou ou se a IA se desculpou
    if not context_found or "Sinto muito, mas não encontrei" in answer:
        confidence = False
        
    return {"confidence": confidence}

# Node para lidar com perguntas muito amplas ou genéricas, onde o modelo pode não ter contexto suficiente para responder de forma precisa
def ask_context_node(state: AgentState) -> AgentState:
    return {
        "answer": "Desculpe, mas não tenho informações suficientes para responder a essa pergunta. Por favor, entre em contato com nosso atendimento para obter assistência personalizada.",
        "citations": [],
        "final_action": "ASK_CONTEXT"
    }

# Transição para atendimento humano caso a IA não tenha confiança na resposta
def human_handoff_node(state: AgentState) -> AgentState:
    intent = state.get("intent")
    
    if intent == "SINISTRO":
        msg = "Parece que sua dúvida está relacionada a um sinistro. Vou transferir você para um de nossos especialistas em sinistros para melhor assistência."
    else:
        msg = "A minha base de conhecimento atual não possui todas as informações necessárias com o grau de segurança exigido. Vou encaminhar o seu contato para a nossa equipe de especialistas."

    return {
        "answer": msg,
        "final_action": "HUMAN_HANDOFF"
    }

# >>> ROTEAMENTO CONDICIONAL
# O Roteamento Condicional atua como o "cérebro" decisório do LangGraph.
# Em vez de seguir um script linear e fixo, estas funções avaliam o estado 
# atual da conversa (a intenção do utilizador, a confiança da IA e a 
# qualidade da pergunta) e funcionam como um "guarda-vias", direcionando 
# o fluxo dinamicamente para o nó mais seguro e adequado.
# Isso garante os Guardrails da aplicação, evitando alucinações.

def route_after_intent(state: AgentState) -> str:
    """Direciona o fluxo baseado na primeira classificação de intenção."""
    if state.get("intent") == "SINISTRO":
        return "human_handoff"
    return "knowledge_retrieval"

def route_after_check(state: AgentState) -> str:
    """
    Avalia a confiança da resposta e o tamanho da pergunta para decidir o destino.
    """
    if state.get("confidence"):
        state["final_action"] = "ANALYSIS_COMPLETE"
        return "end"
    
    question = state.get("question", "").lower()
    word_count = len(question.split())
    
    # Validação rigorosa: Se tem menos de 4 palavras OU possui termos ambíguos
    if word_count < 4 or any(keyword in question for keyword in AMBIGUOUS_KEYWORDS):
        return "ask_context"
    
    return "human_handoff"