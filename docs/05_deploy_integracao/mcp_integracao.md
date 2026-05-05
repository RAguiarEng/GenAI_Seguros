# Integração MCP - GenAI Seguros

## 1. Visão Geral
Utilizamos o **Model Context Protocol (MCP)** como padrão aberto para conectar nosso LLM a ferramentas e dados externos. Isso substitui integrações manuais por um protocolo unificado que facilita a expansão das capacidades do ChatBot.

## 2. Arquitetura MCP
*   **Client:** IDE Antigravity / Agentic Framework.
*   **Protocol:** Transporte de mensagens via stdio ou JSON-RPC.
*   **Servers:** Servidores específicos para funções de seguros.

## 3. Servidores e Ferramentas (Roadmap)
*   **Local Knowledge Server:** Permite ao agente navegar e ler arquivos na pasta `/data` (manuais e apólices).
*   **Search Server:** Integração com APIs de busca (ex: Brave Search ou Serper) para consultar atualizações regulatórias em tempo real.
*   **Database Server:** Conexão futura com o CRM da seguradora para personalização de dados do segurado.

## 4. Segurança e Padronização
O uso de MCP garante que o acesso aos arquivos locais seja feito de forma controlada e auditável, seguindo as melhores práticas de privacidade de dados.