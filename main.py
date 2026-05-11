from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def query():
    db_path = "db"
    
    # Instancia o embedding usado na criação e aponta para a pasta do banco
    embedding_function = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=db_path, embedding_function=embedding_function)
    
    question = input("Escreva sua pergunta: ")
    
    # Busca por similaridade no banco Chroma
    resultados = db.similarity_search_with_relevance_scores(question, k=3)
    if not resultados or resultados[0][1] < 0.7:
        print("Não consegui encontrar informação relevante na base.")
        return
        
    # Junta os fragmentos encontrados para formar o contexto da IA
    retrieved_texts = [resultado[0].page_content for resultado in resultados]
    knowledge_base = "\n\n----\n\n".join(retrieved_texts)
    
    # Template de injeção de contexto (o cerne do RAG)
    prompt_template = ChatPromptTemplate.from_template(
        "Responda à pergunta do usuário com base nas informações abaixo:\n\n{knowledge_base}\n\nPergunta: {question}"
    )
    prompt = prompt_template.invoke({"question": question, "knowledge_base": knowledge_base})
    
    # Envia o prompt processado para a LLM
    model = ChatGoogleGenerativeAI(model="gemini-1.5-flash")    
    answer_text = model.invoke(prompt).content
    
    print(f"\nResposta da IA: {answer_text}")

if __name__ == "__main__":
    query()