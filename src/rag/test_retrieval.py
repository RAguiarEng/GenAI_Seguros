import time
import pandas as pd
from tqdm.auto import tqdm
from langchain_ollama import ChatOllama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from src.rag.vector_store import load_retriever
from src.config import GOOGLE_API_KEY

def test_retrieval(): 
    df = pd.read_csv('data/raw/FAQ.csv')
    retriever = load_retriever("data/vector_store")

    if not retriever:
        print("Nenhum retriever encontrado. Verifique se o vector store foi criado corretamente.")
        return
    
    llm_judge = ChatGoogleGenerativeAI(
        model="gemini-1.5-flash",
        temperature=0,
        api_key=GOOGLE_API_KEY
    )

    # Prompt para avaliar a relevância dos documentos retornados
    prompt_judge = ChatPromptTemplate.from_template(
        """
        És um juiz a avaliar um sistema de recuperação de informação (RAG).\n
        Pergunta do utilizador: {question}\n
        Resposta correta esperada: {expected_answer}\n
        Contexto recuperado pelo sistema: {context}\n\n
        Com base APENAS no contexto recuperado, é possível chegar à resposta correta esperada? 
        Responde estritamente com 'SIM' ou 'NAO'.
        """
    )

    chain_judge = prompt_judge | llm_judge

    correct_answers = 0
    total = len(df)
    batch_size = 5

    print("Iniciando avaliação do sistema de recuperação de informação (RAG)...")
    
    # 3. Iteração em lotes com tratamento de erro 429
    for i in tqdm(range(0, len(df), batch_size)):
        batch = df[i:i + batch_size]
        
        for index, row in batch.iterrows():
            question = row['pergunta']
            expected_answer = row['resposta']

            while True:
                try:
                    # 1ª Chamada de API: Busca na base vetorial (Embeddings)
                    retrieved_docs = retriever.invoke(question)
                    context = "\n\n".join([doc.page_content for doc in retrieved_docs])

                    # 2ª Chamada de API: Avaliação pelo LLM Juiz
                    evaluation = chain_judge.invoke({
                        "question": question,
                        "expected_answer": expected_answer,
                        "context": context
                    }).content.strip().upper()

                    if "SIM" in evaluation:
                        correct_answers += 1
                        
                    break # Sai do loop while True se a requisição for bem-sucedida

                except Exception as e:
                    # Captura o erro 429 independente se vier do Embedding ou do LLM Core
                    if "429" in str(e) or "ResourceExhausted" in str(e):
                        print(f"\nCota de API atingida na pergunta '{question[:20]}...'. Aguardando 61s...")
                        time.sleep(61)
                    else:
                        print(f"\nErro inesperado: {e}")
                        raise e
                        
        # Pequeno intervalo opcional entre os lotes para evitar picos muito rápidos
        time.sleep(2)

    sucess_rate = (correct_answers / total) * 100
    print(f"\n=== Resultado Final da Avaliação ===")
    print(f"Acertos: {correct_answers} de {total}")
    print(f"Taxa de Sucesso: {sucess_rate:.2f}%")

if __name__ == "__main__":
    test_retrieval()