# Arquitetura do Sistema - GenAI Seguros

## 1. Visão Geral
Este sistema é projetado como um **Sistema de IA Composto**, utilizando a arquitetura **RAG** para garantir que as respostas do chatbot de seguros sejam fundamentadas em documentos oficiais e técnicos, reduzindo alucinações.

## 2. Pilares do Sistema
*   **Ingestão:** Processamento de manuais (PDF/MD) reais de seguradora.
*   **Recuperação:** Busca semântica em banco de dados vetorial.
*   **Geração:** Uso de LLMs de última geração para síntese de respostas.
*   **Protocolo:** Uso de MCP para conexão entre o modelo cloud e arquivos locais.

## 3. Fluxo de Dados de Alto Nível
[Pergunta Usuário] -> [Consulta Vetorial] -> [Contexto Extraído] -> [LLM] -> [Resposta Grounded]

## 4. Stack Tecnológica Proposta
As seguintes tecnologias são propostas como ponto de partida para o desenvolvimento do MVP (Minimum Viable Product):
*   **Interface de Usuário:** [Streamlit](https://streamlit.io/) para criação rápida do dashboard do chatbot.
*   **Banco de Dados Vetorial:** [FAISS](https://github.com/facebookresearch/faiss) para indexação e busca semântica eficiente.
*   **Orquestração de IA:** [LangChain](https://www.langchain.com/) ou [LlamaIndex](https://www.llamaindex.ai/) para gerenciar o fluxo de RAG.

*Nota: Esta stack representa uma recomendação inicial e pode ser ajustada conforme a evolução do projeto.*