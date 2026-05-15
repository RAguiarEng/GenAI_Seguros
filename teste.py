import streamlit as st
from src.config import VECTOR_STORE_DIR
from src.rag.vector_store import load_retriever
from src.bot.graph import compile_agent

@st.cache_resource
def init_agent():
    retriever = load_retriever(VECTOR_STORE_DIR)
    if not retriever:
        return None
    return compile_agent(retriever)

st.set_page_config(page_title="GenAI Seguros", page_icon="🛡️", layout="centered")

# Sidebar para Status e Controles
with st.sidebar:
    st.markdown("### 📊 Status do Sistema")
    st.success("✅ Banco Vetorial: Conectado (ChromaDB)")
    st.success("✅ Modelo de LLM: Gemini Ativo")
    st.success("✅ Motor: LangGraph Agent")
    
    st.markdown("---")
    if st.button("🗑️ Limpar Conversa"):
        st.session_state.messages = [{"role": "assistant", "content": "Como posso ajudar com o seu seguro hoje?"}]
        st.rerun()

st.title("🛡️ GenAI Seguros")
st.markdown("Olá! Sou o assistente de IA da seguradora. Estou aqui para tirar suas dúvidas com base nos Manuais e Apólices oficiais.")

agent = init_agent()

if not agent:
    st.warning(">>> A base de conhecimento da seguradora ainda não foi carregada. Por favor, processe os documentos PDF.")
    st.stop()

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Como posso ajudar com o seu seguro hoje?"}]

# Exibe o histórico com avatares customizados
for msg in st.session_state.messages:
    avatar = "👤" if msg["role"] == "user" else "🤖"
    with st.chat_message(msg["role"], avatar=avatar):
        st.markdown(msg["content"])

if user_input := st.chat_input("Ex: Quais são as coberturas básicas do Vida Flex?"):
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user", avatar="👤"):
        st.markdown(user_input)

    with st.chat_message("assistant", avatar="🤖"):
        with st.spinner("Consultando manuais e apólices..."):
            state_response = agent.invoke({"question": user_input})
            
            answer_text = state_response.get("answer", "Ocorreu um erro ao processar sua solicitação.")
            citations = state_response.get("citations", [])
            
            st.markdown(answer_text)
            
            if citations:
                with st.expander("📚 Fontes Oficiais Encontradas"):
                    for c in citations:
                        st.markdown(f"**{c.get('document', 'Desconhecido')}** (Pág. {c.get('page', 'N/A')})\n> _{c.get('snippet', '')}_")
            
            st.session_state.messages.append({"role": "assistant", "content": answer_text})
