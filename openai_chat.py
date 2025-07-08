from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def formatar_com_gpt(texto: str) -> dict:
    try:
        response = client.responses.create(
            model="gpt-4.1",
            instructions="Você é um assistente que transforma PDFs de músicas gospel em JSON estruturado com as chaves: 'titulo', 'autor' e 'cifra'.",
            input=texto
        )

        conteudo = response.output_text.strip()
        return eval(conteudo)

    except Exception as e:
        print("Erro GPT:", e)
        return {"titulo": "Erro", "autor": "Erro", "cifra": "Erro"}
