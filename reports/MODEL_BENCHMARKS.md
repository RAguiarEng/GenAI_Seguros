# Benchmarks de Modelos - GenAI Seguros

## 1. Objetivo
Comparar o desempenho de LLMs locais e em nuvem para identificar o melhor motor de inferência para o atendimento de seguros GenAI Seguros, priorizando a ausência de alucinações.

## 2. Modelos Avaliados
*   **Local:** Gemma:2b (Ollama).
*   **Cloud (API):** Gemini 1.5 Pro, Llama 3.1 (70B), DeepSeek R1 (Thinking).

## 3. Matriz Comparativa (Dados de Referência)

| Modelo | Local/Cloud | Acurácia (Golden Set) | Latência (Média) | Custo (1M tokens) |
| :--- | :--- | :--- | :--- | :--- |
| **Gemma:2b** | Local | (Pendente) | (Pendente) | $0.00 |
| **Llama 3.1 70B** | Cloud | (Pendente) | (Pendente) | $0.60 |
| **DeepSeek R1** | Cloud | (Pendente) | (Pendente) | $2.00 |

## 4. Observações Técnicas
*   **Modelos de Raciocínio (DeepSeek/o3):** Devem ser preferidos para análise de exclusões de apólice devido ao processo de "cadeia de pensamento" interno.
*   **Modelos Locais:** Úteis para triagem inicial de intenções simples para garantir privacidade total dos dados sensíveis do segurado.

## 5. Recomendação Provisória
No estágio atual, recomenda-se o uso de modelos Cloud para a fase de geração final do RAG devido à complexidade gramatical e jurídica dos manuais GenAI Seguros.