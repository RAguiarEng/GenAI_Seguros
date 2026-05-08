from langchain_chroma import Chroma
from langchain_google_genai import ChatGoogleGenerativeAI, GoogleGenerativeAIEmbeddings
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

def perguntar():
    caminho_db = "db"
    
    # Instancia o embedding usado na criação e aponta para a pasta do banco
    funcao_embedding = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    db = Chroma(persist_directory=caminho_db, embedding_function=funcao_embedding)
    
    pergunta = input("Escreva sua pergunta: ")
    
    # Busca por similaridade no banco Chroma
    resultados = db.similarity_search_with_relevance_scores(pergunta, k=3)
    if not resultados or resultados[0][1] < 0.7:
        print("Não consegui encontrar informação relevante na base.")
        return
        
    # Junta os fragmentos encontrados para formar o contexto da IA
    textos_resultados = [resultado[0].page_content for resultado in resultados]
    base_conhecimento = "\n\n----\n\n".join(textos_resultados)
    
    # Template de injeção de contexto (o cerne do RAG)
    prompt_template = ChatPromptTemplate.from_template(
        "Responda à pergunta do usuário com base nas informações abaixo:\n\n{base_conhecimento}\n\nPergunta: {pergunta}"
    )
    prompt = prompt_template.invoke({"pergunta": pergunta, "base_conhecimento": base_conhecimento})
    
    # Envia o prompt processado para a LLM
    modelo = ChatGoogleGenerativeAI(model="gemini-1.5-flash")    
    texto_resposta = modelo.invoke(prompt).content
    
    print(f"\nResposta da IA: {texto_resposta}")

if __name__ == "__main__":
    perguntar()