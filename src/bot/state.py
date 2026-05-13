from typing import List, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict, total=False):
    question: str           # pergunta do usuário
    answer: Optional[str]   # resposta gerada pelo modelo
    citations: List[dict]   # lista de citações (documento, página, trecho)
    conext_found: bool      # indica se o contexto relevante foi encontrado nos documentos
    final_action: str       # ação final do node (ex: ANALYSIS_COMPLETE, HUMAN_HANDOFF)
    intent: str             # intenção detectada (ex: sinistro, FAQ)
    confidence: bool        # confiança na resposta para evitar alucinações