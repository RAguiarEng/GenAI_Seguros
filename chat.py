import streamlit as st

def main(): 
    
    st.set_page_config(page_title="GenAI Seguros - Chatbot de Atendimento", page_icon=":robot:")

    with st.sidebar:
        st.title("GenAi Seguros")

        st.divider() # Linha de separação

        # Seção de Perguntas Frenquentes
        st.header("Perguntas Frequentes")

        st.markdown("- Como acionar o sinistro?")
        st.markdown("- Coberturas disponíveis")
        st.markdown("- Alterar dados da apólice")
        st.markdown("- Segunda via de boleto")
        st.markdown("- Telefones úteis")
        
# --- ÁREA PRINCIPAL (Chat) ---

# 2. Inicializar o histórico de mensagens se for a primeira vez que a página carrega
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "assistant",
            "content": "Olá! Sou o assistente da GenAI Seguros. Estou aqui para ajudar com as suas dúvidas sobre coberturas e serviços.\n\nO que você precisa hoje?"
        }
    ]

# 3. Exibir as mensagens que estão no histórico
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# --- ENTRADA DE TEXTO (Input Area) ---

# Criamos um "Popover" que funciona como um botão. Quando clicado, revela o uploader.
with st.popover("📎 Anexar arquivo"):
    arquivo_anexado = st.file_uploader(
        "Selecione um documento ou imagem", 
        type=["pdf", "jpg", "jpeg", "png", "docx"] # Defina os formatos aceitos
    )
    if arquivo_anexado is not None:
        st.success(f"Arquivo '{arquivo_anexado.name}' pronto para envio!")

# 4. Campo de digitação de dúvidas
prompt = st.chat_input("Digite sua dúvida aqui...")

if prompt:
    # Mostra a mensagem do usuário na tela e salva no histórico
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
        
        # Se o usuário enviou um arquivo junto com a mensagem, mostramos isso no chat
        if arquivo_anexado is not None:
            st.info(f"📎 Arquivo enviado: {arquivo_anexado.name}")
    
    # --- LÓGICA DO BOT ---
    # Aqui entra a inteligência da sua GenAI
    if arquivo_anexado:
        resposta_bot = f"Recebi sua mensagem: '{prompt}' e também vi que você anexou o arquivo **{arquivo_anexado.name}**. Vou analisar o documento!"
    else:
        resposta_bot = f"Você disse: '{prompt}'. Estou processando sua dúvida!"
    
    # Mostra a resposta do assistente na tela e salva no histórico
    st.session_state.messages.append({"role": "assistant", "content": resposta_bot})
    with st.chat_message("assistant"):
        st.markdown(resposta_bot)

if __name__ == "__main__":
    main()