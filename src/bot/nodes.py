from src.bot.state import AgentState
from src.rag.chain import get_rag_chain, format_citations

def get_knowledge_retrieval_node(retriever):
    def retrieve_node(state: AgentState) -> AgentState:
        question = state.get("question", "")
        # Apenas busca os documentos, sem tomar decisões de UX aqui
        docs = retriever.invoke(question)
        return {"context_docs": docs}  # Assumindo que você adicione 'context_docs' ao state.py, ou reutilize 'citations'
    return retrieve_node

def get_generation_node():
    chain = get_rag_chain()
    
    def generate_node(state: AgentState) -> AgentState:
        question = state.get("question", "")
        docs = state.get("context_docs", []) # Recupera os documentos buscados no nó anterior
        
        # A IA recebe a missão de ler, analisar e formatar a saída.
        # Se os docs estiverem vazios, a própria IA saberá dar a resposta de fallback baseada no nosso Prompt de Sistema.
        answer = chain.invoke({
            "question": question,
            "context": docs,
            "docs": docs
        })
        
        return {
            "answer": answer,
            "citations": format_citations(docs, question) if docs else [],
            "final_action": "ANALYSIS_COMPLETE"
        }
    return generate_node
