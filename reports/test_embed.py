# test_embed.py
import os
from dotenv import load_dotenv
from google import genai

load_dotenv()

api_key = os.environ.get("GOOGLE_API_KEY")
if not api_key:
    raise RuntimeError("GOOGLE_API_KEY não definida")

EMBEDDING_MODEL = os.environ.get("EMBEDDING_MODEL", "text-embedding-004")

client = genai.Client(api_key=api_key)

def main():
    text = "Teste de embedding para o projeto de seguros."
    print(f"Usando modelo de embedding: {EMBEDDING_MODEL}\n")

    resp = client.models.embed_content(
        model=EMBEDDING_MODEL,
        contents=text,
    )

    print("Resposta bruta:")
    print(resp)
    try:
        vector = resp.embeddings[0].values
        print(f"\nTamanho do vetor: {len(vector)}")
        print(f"Primeiros 5 valores: {vector[:5]}")
    except Exception as e:
        print("Não consegui acessar o vetor de embeddings diretamente:", e)

if __name__ == "__main__":
    main()