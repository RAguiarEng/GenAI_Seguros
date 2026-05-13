import streamlit as st
from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

# Função para inicializar o agente com cache para evitar recarregamentos desnecessários
@st.cache_resource
def init_agent():
    retriever = load_retriever(VECTOR_STORE_DIR)
    if not retriever:
        return None
    return compile_agent(retriever)

# Configuração da Página
st.set_page_config(page_title="GenAI Seguros", page_icon="🤖", layout="centered")
st.title("🚀 GenAI Seguros")
st.markdown("Olá! Sou o seu assistente inteligente. Estou aqui para tirar suas dúvidas sobre apólices, coberturas e acionamento de sinistros de forma rápida e descomplicada.")

agent = init_agent()

# Verificação se o agente foi inicializado corretamente
if not agent:
    st.warning(">>> A base de conhecimento da seguradora ainda não foi carregada. Por favor, processe os documentos PDF.")
    st.stop()

# Inicializa o histórico na sessão (messages em vez de mensagens)
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Como posso ajudar com o seu seguro hoje?"}]

# Exibe o histórico de chat
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Recebe a pergunta do segurado
if user_input := st.chat_input("Ex: Como funciona a cobertura para doenças graves?"):
    
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Processa a resposta
    with st.chat_message("assistant"):
        with st.spinner("Consultando as condições gerais..."):
            
            # Passa a pergunta usando 'question'
            state_response = agent.invoke({"question": user_input})
            
            # Recupera as chaves em inglês
            answer_text = state_response.get("answer", "Ocorreu um erro ao processar sua solicitação.")
            citations = state_response.get("citations", [])
            
            st.markdown(answer_text)
            
            # Mostra o embasamento legal/condições gerais
            if citations:
                with st.expander("📄 Trechos do Manual/Apólice"):
                    for c in citations:
                        st.markdown(f"**{c.get('document', 'Desconhecido')} (Pág {c.get('page', 'N/A')})**\n_{c.get('snippet', '')}_")
            
            # Salva a resposta da IA no histórico
            st.session_state.messages.append({"role": "assistant", "content": answer_text})