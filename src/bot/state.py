from typing import List, Optional
from typing_extensions import TypedDict

class AgentState(TypedDict, total=False):
    pergunta: str
    resposta: Optional[str]
    citacoes: List[dict]
    contexto_encontrado: bool
    acao_final: str