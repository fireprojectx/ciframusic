from openai import OpenAI, APIError, APIConnectionError, RateLimitError
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

    except APIError as e:
        print(f"Erro da API OpenAI: {e}")
    except APIConnectionError as e:
        print(f"Erro de conexão com a OpenAI: {e}")
    except RateLimitError as e:
        print(f"Rate limit excedido: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return {"titulo": "Erro", "autor": "Erro", "cifra": "Erro"}
