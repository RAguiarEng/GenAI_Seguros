import re
import pathlib
from typing import List, Dict

from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_ollama import ChatOllama
from langchain_core.prompts import ChatPromptTemplate
from langchain_classic.chains.combine_documents import create_stuff_documents_chain

# Importa as configurações ajustadas do config.py
from src.config import GOOGLE_API_KEY, LLM_MODEL, LLM_PROVIDER, OLLAMA_MODEL
from src.bot.prompts import SYSTEM_PROMPT, USER_PROMPT_KNOWLEDGE

# Função para obter a LLM configurada (Google Gemini ou Ollama local)
def get_llm():
    if LLM_PROVIDER == "local":
        print(f"Usando LLM local com modelo: {OLLAMA_MODEL}")
        return ChatOllama(
            model=OLLAMA_MODEL, 
            temperature=0.0)

    elif LLM_PROVIDER == "google":
        print(f"Usando Google Gemini como LLM com modelo: {LLM_MODEL}")
        return ChatGoogleGenerativeAI(
            model=LLM_MODEL,
            temperature=0.0,
            api_key=GOOGLE_API_KEY
        )
    else:
        raise ValueError(f"Provedor de LLM desconhecido: {LLM_PROVIDER}")

# Função para criar a cadeia RAG usando a LLM configurada e os prompts definidos
def get_rag_chain():
    llm = get_llm()

    prompt = ChatPromptTemplate.from_messages([
        ("system", SYSTEM_PROMPT),
        ("human", f"{USER_PROMPT_KNOWLEDGE}\n\nContexto dos Documentos:\n{{context}}")
    ])
    
    return create_stuff_documents_chain(llm, prompt)

# Função para formatar as citações dos documentos relacionados à pergunta do usuário
def format_citations(docs_rel: List, query: str) -> List[Dict]:
    def _clean_text(s: str) -> str:
        return re.sub(r"\s+", " ", s or "").strip()

    def _extract_snippet(texto: str, query: str, janela: int = 300) -> str:
        txt = _clean_text(texto)
        pos = txt.lower().find(query.lower()[:50])
        if pos == -1: pos = 0
        ini = max(0, pos - janela//2)
        fim = min(len(txt), pos + janela//2)
        return f"...{txt[ini:fim]}..."

    cites, seen_docs = [], set()
    for d in docs_rel:
        src = pathlib.Path(d.metadata.get("source", "")).name
        if src not in seen_docs:
            page = int(d.metadata.get("page", 0)) + 1
            cites.append({
                "documento": src, 
                "pagina": page, 
                "trecho": _extract_snippet(d.page_content, query)
            })
            seen_docs.add(src)
    return cites[:3]