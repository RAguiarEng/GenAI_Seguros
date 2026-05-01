# GenAI Seguros - Desafio 2 (InsurMinds)

Bem-vindo ao repositório do **ChatBot de Atendimento** da equipe! Este projeto faz parte da Atividade Obrigatória 2 do curso InsurMinds (I2A2).

## 🎯 Objetivo do Projeto
Desenvolver um chatbot (assistente virtual) baseado em Inteligência Artificial para automatizar o atendimento ao segurado. O foco é responder a perguntas frequentes e direcionar solicitações, proporcionando respostas rápidas e liberando a equipe humana para casos mais complexos.

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
