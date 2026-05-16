import uvicorn 
import os

# Inicializa o serviço do FastAPI
if __name__ == "__main__":
    print("Iniciando servidor GenAI Seguros...")      
    print(os.environ.get("GEMINI_API_KEY"))    
    uvicorn.run(
        "src.api.chat_endpoint:app", 
        host="0.0.0.0", 
        port=8000,      
        reload=True     
    )