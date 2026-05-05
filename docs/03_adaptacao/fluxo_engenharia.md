# Engenharia de Fluxo - GenAI Seguros

## 1. Mentalidade do Fluxo
O ChatBot opera sob a lógica de **Flow Engineering**, utilizando estados para garantir que o atendimento ao segurado seja preciso e seguro. Em vez de uma resposta direta, o sistema avalia a intenção e a qualidade da informação antes de responder.

## 2. Estados do Sistema (Nodes)
*   **START:** Recebimento da query do segurado.
*   **INTENT_ROUTING:** Classificação da dúvida (Sinistro, FAQ, Financeiro).
*   **KNOWLEDGE_RETRIEVAL:** Busca semântica nos manuais da seguradora via RAG.
*   **ANSWER_CHECK:** Verificação de fidelidade (groundedness) para evitar alucinações.
*   **HUMAN_HANDOFF:** Transição para atendimento humano caso a IA não tenha confiança na resposta.

## 3. Diagrama Lógico (Provisório)
[Entrada] -> [Classificador] --(FAQ)--> [RAG] -> [Validador] -> [Resposta]
                              |
                        (Sinistro) -> [Encaminhar Humano]