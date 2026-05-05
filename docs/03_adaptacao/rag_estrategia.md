# Estratégia de RAG - GenAI Seguros

## 1. Fontes de Conhecimento
Para este projeto, a base de conhecimento é dividida por níveis de criticidade:
*   **FAQs Seguros:** Utilizados para suporte a dúvidas gerais e linguagem natural.
*   **Manuais de Processos:** Instruções sobre fluxos operacionais (ex: como abrir um sinistro).
*   **Termos e Condições de Apólices:** A **"Fonte da Verdade Jurídica"**. Contém as cláusulas, exclusões e limites de cobertura que regem o contrato.

## 2. Processamento e Higienização de Dados
A qualidade da recuperação depende da integridade do texto processado:
*   **Limpeza Técnica:** Remoção de ruídos de PDF (cabeçalhos, números de página, marcas d'água) que podem confundir o retriever.
*   **Chunking (Fragmentação):** Os documentos serão divididos em blocos semânticos (500-1000 tokens).
    *   *Regra de Ouro:* Evitar quebras no meio de cláusulas jurídicas para não perder o contexto da obrigação ou direito.
*   **Vetorização:** Uso de modelos de embedding para capturar o significado semântico, garantindo que "sinistro" e "acidente" sejam relacionados corretamente.

## 3. Mecanismo de Busca e Recuperação (Retriever)
*   **Banco Vetorial:** Proposta inicial via **FAISS** (Facebook AI Similarity Search) para armazenamento e busca de alta performance. 
    *   *Nota:* Esta é uma proposta técnica inicial, sujeita a validação durante a fase de desenvolvimento.
*   **Busca por Similaridade:** O sistema recuperará os trechos mais relevantes (Top-K) para compor o prompt.
*   **Metadados:** Cada fragmento será indexado com metadados (nome do documento, página, seção) para permitir citações diretas na resposta final.

## 4. Avaliação de Qualidade e Groundedness
Para garantir que o modelo não invente informações (alucinação), aplicaremos:
*   **Fidelidade (Faithfulness):** Verificação se a resposta gerada está estritamente fundamentada nos documentos recuperados.
*   **Relevância:** Garantir que o contexto recuperado realmente responde à dor do segurado.

## ⚠️ PONTO DE ATENÇÃO: Segurança Jurídica e Conformidade
Devido à natureza do setor de seguros, o sistema deve seguir diretrizes rigorosas para evitar riscos legais:

1.  **Prioridade da Apólice:** Em caso de conflito entre o FAQ e as Condições Gerais da Apólice, o dado da apólice prevalece como a verdade absoluta.
2.  **Citação de Fontes:** O ChatBot deve ser instruído a citar de qual manual ou seção da apólice retirou a informação (Ex: *"Conforme a Cláusula 5.2 do Manual do Segurado..."*).
3.  **Abstenção de Especulação:** Se a informação não estiver presente no contexto recuperado, o agente deve declarar que não sabe e solicitar que o usuário forneça o documento ou procure um atendente humano.
4.  **Prevenção de Alucinações Jurídicas:** O validador de saída deve focar em identificar termos que não existem no contrato original para evitar promessas indevidas de cobertura.