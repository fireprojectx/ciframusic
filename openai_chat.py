import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

def formatar_com_gpt(texto: str) -> dict:
    try:
        resposta = openai.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": "Você é um assistente que transforma PDFs de músicas gospel em JSON estruturado com as chaves: 'titulo', 'autor' e 'cifra'."
                },
                {
                    "role": "user",
                    "content": texto
                }
            ],
            temperature=0.2
        )

        conteudo = resposta.choices[0].message.content.strip()
        return eval(conteudo)

    except Exception as e:
        print("Erro GPT:", e)
        return {"titulo": "Erro", "autor": "Erro", "cifra": "Erro"}


