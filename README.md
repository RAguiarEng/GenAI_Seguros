# GenAI Seguros - Desafio 2 (InsurMinds)

Bem-vindo ao repositório do **ChatBot de Atendimento** da equipe! Este projeto faz parte da Atividade Obrigatória 2 do curso InsurMinds (I2A2).

## 🎯 Objetivo do Projeto
Desenvolver um chatbot (assistente virtual) baseado em Inteligência Artificial para automatizar o atendimento ao segurado. O foco é responder a perguntas frequentes e direcionar solicitações, proporcionando respostas rápidas e liberando a equipe humana para casos mais complexos.

**Visite nossa página: [GenAI Seguros](https://raguiareng.github.io/GenAI_Seguros/).**

## 📂 Estrutura do Projeto
Para garantir a rastreabilidade e a colaboração eficiente, o repositório está organizado da seguinte forma:

```text
GenAI_Seguros/
├── data/                       # Pipeline de Dados (Camadas Raw, Processed e Vector)
│   ├── raw/                    # Dados brutos e originais (ex: PDFs de manuais, FAQs)
│   ├── processed/              # Dados limpos e pré-processados para RAG
│   └── vector_store/           # Banco de dados vetorial (embeddings)
├── docs/                       # Documentação seguindo o Ciclo de Vida da IA Generativa
│   ├── 01_escopo/              # Documentos de escopo e fontes de conhecimento iniciais
│   ├── 02_selecao/             # Documentos relacionados à seleção de modelos e ferramentas
│   ├── 03_adaptacao/           # Estratégias de RAG e engenharia de fluxo (ex: fluxo_engenharia.md, rag_estrategia.md)
│   ├── 04_avaliacao/           # Métricas e planos de avaliação do chatbot
│   └── 05_deploy_integracao/   # Arquitetura e planos de deploy/integração (ex: arquitetura.md, mcp_integracao.md)
├── notebooks/                  # Experimentação, prototipagem e testes rápidos de prompts
├── reports/                    # Relatórios de progresso, métricas de qualidade e logs de auditoria
├── src/                        # Código-fonte modularizado
│   ├── api/                    # Interface do chatbot (ex: Streamlit)
│   ├── bot/                    # Lógica principal do chatbot e gestão de prompts
│   ├── data_ingestion/         # Módulos para ingestão e pré-processamento de dados
│   ├── evaluation/             # Módulos para avaliação de desempenho do chatbot
│   └── rag/                    # Módulos para Retrieval-Augmented Generation (retriever)
├── .gitignore                  # Arquivos ignorados pelo Git
├── LICENSE                     # Licença do projeto
├── README.md                   # Documentação principal do projeto
└── orientativo_github.md       # Guia prático de colaboração e uso do GitHub
```

*   **`data/`**: Contém os dados em diferentes estágios de processamento para o RAG.
    *   `raw/`: Armazena os documentos originais, como PDFs de manuais e FAQs.
    *   `processed/`: Guarda os dados após limpeza e formatação, prontos para vetorização.
    *   `vector_store/`: Onde o banco de dados vetorial (ex: FAISS) é armazenado.
*   **`docs/`**: Organizado por fases do ciclo de vida da IA Generativa.
    *   `01_escopo/`: Define o escopo do projeto e as fontes de conhecimento iniciais.
    *   `02_selecao/`: Detalha a escolha de modelos e ferramentas.
    *   `03_adaptacao/`: Inclui documentos sobre estratégias de RAG e engenharia de fluxo.
    *   `04_avaliacao/`: Contém planos e resultados de avaliação.
    *   `05_deploy_integracao/`: Abriga a arquitetura do sistema e planos de deploy.
*   **`notebooks/`**: Ambiente para experimentação, prototipagem e testes rápidos de prompts e modelos.
*   **`reports/`**: Armazena relatórios de progresso, métricas de qualidade do chatbot (fidelidade, relevância) e logs de auditoria.
*   **`src/`**: Contém o código-fonte modularizado do chatbot.
    *   `api/`: Módulos para a interface do usuário (ex: Streamlit).
    *   `bot/`: Lógica central do chatbot e gerenciamento de prompts.
    *   `data_ingestion/`: Scripts para ingestão e pré-processamento de dados.
    *   `evaluation/`: Ferramentas e scripts para avaliar o desempenho do chatbot.
    *   `rag/`: Implementação do mecanismo de Retrieval-Augmented Generation.

## 📝 O que precisamos fazer
- **Mapear e categorizar** as perguntas frequentes (FAQs) dos segurados.
- **Estruturar fluxos** de atendimento conversacionais.
- **Treinar o modelo de IA (LLM)** utilizando dados históricos, manuais, termos de apólices ou bases do Kaggle.
- Implementar **RAG (Retrieval-Augmented Generation)** para enriquecer o contexto das respostas.
- *(Opcional)* Integrar com histórico de tickets ou sistemas de CRM.

## 📦 Entregáveis da Equipe (Prazo: 29/05/2026)
Todos os arquivos devem ser gerados neste repositório para facilitar o envio:
1. **Artefatos:** Código fonte do chatbot, bases de dados utilizadas, diagramas e documentos de projeto.
2. **Relatório:** Arquivo PDF descrevendo todo o experimento realizado.
3. **Evidências:** Capturas de tela, vídeos ou logs comprovando o funcionamento do ChatBot.
4. **Link:** (Se houver) Link para acesso à versão executável na nuvem.

---

## 🛠️ Guia Rápido do GitHub (Para Iniciantes)

Se você nunca usou o GitHub antes, não se preocupe! Aqui está um resumo prático de como trabalhar no projeto sem quebrar nada. Para mais detalhes, leia o arquivo de documentação [orientativo_github.md](orientativo_github.md).

### 1. Baixando o projeto (Clonando)
Apenas a primeira vez, para colocar os arquivos do projeto no seu computador:
```bash
git clone https://github.com/RAguiarEng/GenAI_Seguros.git
cd GenAI_Seguros
```

### 2. Começando uma tarefa (Branch)
Nunca edite a versão principal (`main`). Crie um "ramo" (branch) separado para você trabalhar com segurança:
```bash
# Atualize sua máquina com a versão mais recente
git checkout main
git pull origin main

# Crie seu ramo de trabalho (substitua o nome `minha-branch` para algo que identifique sua branch)
git checkout -b minha-branch
```

### 3. Salvando seu trabalho (Commit)
Quando fizer alterações nos arquivos e quiser salvar no histórico:
```bash
git add .
git commit -m "Mensagem descrevendo o que eu fiz"
```

### 4. Enviando para a Nuvem (Push)
Para que o resto da equipe veja o seu trabalho no GitHub:
```bash
git push origin minha-branch
```

### 5. Juntando tudo (Pull Request)
Vá até a página do projeto no site do GitHub. Vai aparecer um botão verde pedindo para criar um **Pull Request**. Isso serve para pedir que seu código seja adicionado ao projeto principal (`main`). A equipe revisa e aprova!

>**Dica:** Se achar os comandos de texto complicados, baixe o [GitHub Desktop](https://desktop.github.com/). É um programa visual que faz tudo isso através de botões!
> Qualquer dúvida, comente no nosso grupo do WhatsApp.
