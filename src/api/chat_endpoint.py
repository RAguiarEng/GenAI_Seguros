from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Any, Optional

from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

# Inicializando API
app = FastAPI(title="API GenAI Seguros Chatbot (Gemini)")

# Configuração de CORS para permitir que o seu HTML (frontend) acesse a API
app.add_middleware( 
    CORSMiddleware,         # Permite que o navegador entenda que a comunicação está liberada 
    allow_origins=["*"],    # Define quem tem permissão de conversar com a API. O [*] significa "Permitir qualquer origem"
    allow_credentials=True, # Define se a API permite que o navegador do cliente envie credenciais de requisições de origem cruzada (Cookies, certificados TLS ou Cabeçalhos Authorization)
    allow_methods=["*"],    # Define quais ações (GET, POST, PUT, DELETE ou OPTIONS) o frontend pode executar na API
    allow_headers=["*"],    # Define quais cabeçalhos o frontend pode enviar junto com a requisição
    
    #OBS: Em produção, evitar o uso do coringa [ * ]
)

# Inicialização do Agente
print("Carregando banco vetorial e inicializando o agente...")
retriever = load_retriever(VECTOR_STORE_DIR)
if retriever:
    agent = compile_agent(retriever)
    print("Agente LangGraph inicializado com sucesso!")
else:
    agent = None
    print("Aviso: Base de conhecimento não carregada. Verifique os PDFs.")

# Modelo de dados
class ChatRequest(BaseModel):
    question: str
    session_id: str

class ChatResponse(BaseModel):
    answer: str
    citations: List[Dict[str, Any]] = []

#Rota da API
@app.post("/api/chat/langchain", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not agent:
        raise HTTPException(
            status_code=500, # Internal Server Error
            detail="A base de conhecimento da seguradora ainda não foi carregada. Processe os documentos PDF."
        )        
    try:
        # Em LangGraph, a memória (histórico) geralmente é controlada injetando um 'thread_id' dentro das configurações de execução (config).
        # O LangGraph precisa saber a qual conversa pertence essa execução. Assim, mantém um histórico
        config = {"configurable": {"thread_id": request.session_id}}
        
        # Permite monitorar um timeout para o caso de inatividade do usuário
        if request.question == "__TIMEOUT_PING__": # Estourou o tempo de aguardo da resposta
            # Sistema assume o papel de usuário e injeta uma pergunta
            prompt_inatividade = (
                "[system]: O usuário está inativo há alguns minutos. "
                "Pergunte educadamente se ele ainda está aí e se precisa de mais alguma ajuda com os seguros."
            )
            # Invoca o agente do LangGraph passando a pergunta do sistema e a config da sessão
            state_response = agent.invoke({"question": prompt_inatividade}, config=config)        
        else:     
            # Invoca o agente do LangGraph passando a pergunta do usuário e a config da sessão       
            state_response = agent.invoke({"question": request.question}, config=config)
                
        # Extrai os dados retornados pelo estado do seu grafo
        answer_text = state_response.get("answer", "Ocorreu um erro ao processar sua solicitação.")
        citations = state_response.get("citations", [])
                                
        return ChatResponse(
            answer=answer_text,
            citations=citations
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))