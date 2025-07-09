from openai import OpenAI, APIError, APIConnectionError, RateLimitError
import os
import json

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

def formatar_com_gpt(texto: str) -> dict:
    try:
        response = client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {
                    "role": "system",
                    "content": (
                        "Você é um assistente que transforma letras de músicas gospel em JSON "
                        "com as chaves: 'titulo', 'autor' e 'cifra'. "
                        "A resposta **DEVE** estar formatada como um JSON Python válido. Exemplo:\n"
                        "{\n"
                        "  \"titulo\": \"Porque Ele Vive\",\n"
                        "  \"autor\": \"Desconhecido\",\n"
                        "  \"cifra\": \"[D] Deus enviou Seu Filho a[G]mado\\n[Em] Pra me salvar e per[A]doar\\n...\"\n"
                        "}"
                    )
                },
                {"role": "user", "content": texto}
            ],
            temperature=0.3
        )

        conteudo = response.choices[0].message.content.strip()

        try:
            return json.loads(conteudo)
        except json.JSONDecodeError:
            print("❌ Erro ao decodificar JSON retornado pela API.")
            print("Conteúdo recebido:\n", conteudo)

    except APIError as e:
        print(f"Erro da API OpenAI: {e}")
    except APIConnectionError as e:
        print(f"Erro de conexão com a OpenAI: {e}")
    except RateLimitError as e:
        print(f"Rate limit excedido: {e}")
    except Exception as e:
        print(f"Erro inesperado: {e}")

    return {"titulo": "Erro", "autor": "Erro", "cifra": "Erro"}
