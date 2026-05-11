import streamlit as st
from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

# Cache do Agente: Evita recarregar o ChromaDB a cada mensagem
@st.cache_resource
def iniciar_agente():
    retriever = load_retriever(VECTOR_STORE_DIR)
    if not retriever:
        return None
    return compile_agent(retriever)

# Configuração da Página
st.set_page_config(page_title="GenAI Seguros", page_icon="☂️", layout="centered")
st.title("☂️ GenAI Seguros")
st.markdown("Olá! Sou o seu assistente inteligente. Estou aqui para tirar suas dúvidas sobre apólices, coberturas e acionamento de sinistros de forma rápida e descomplicada.")

agente_seguros = iniciar_agente()

if not agente_seguros:
    st.warning("⚠️ A base de conhecimento da seguradora ainda não foi carregada. Por favor, processe os documentos PDF (rode o script de criação do DB).")
    st.stop()

# Inicializa o histórico na sessão
if "mensagens" not in st.session_state:
    st.session_state.mensagens = [{"role": "assistant", "content": "Como posso ajudar com o seu seguro de vida hoje?"}]

# Exibe o histórico de chat
for msg in st.session_state.mensagens:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Recebe a pergunta do segurado
if pergunta := st.chat_input("Ex: Como funciona a cobertura para doenças graves?"):
    
    st.session_state.mensagens.append({"role": "user", "content": pergunta})
    with st.chat_message("user"):
        st.markdown(pergunta)

    # Processa a resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando as condições gerais..."):
            resposta_agente = agente_seguros.invoke({"pergunta": pergunta})
            
            texto_resposta = resposta_agente.get("resposta", "Ocorreu um erro ao processar sua solicitação.")
            citacoes = resposta_agente.get("citacoes", [])
            
            st.markdown(texto_resposta)
            
            # Mostra o embasamento legal/condições gerais
            if citacoes:
                with st.expander("📄 Trechos do Manual/Apólice"):
                    for c in citacoes:
                        st.markdown(f"**{c['documento']} (Pág {c['pagina']}):**")
                        st.caption(f"> {c['trecho']}")
            
            st.session_state.mensagens.append({"role": "assistant", "content": texto_resposta})