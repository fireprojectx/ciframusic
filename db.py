import psycopg2
import os
from dotenv import load_dotenv

# Carrega as variáveis do .env (caso esteja rodando localmente ou no Codespaces)
load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def salvar_cifra(titulo, autor, cifra):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO cifras (titulo, autor, cifra)
                    VALUES (%s, %s, %s)
                    """,
                    (titulo, autor, cifra)
                )
    except Exception as e:
        print("❌ Erro ao salvar cifra no banco:", e)

def listar_cifras():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, titulo, autor FROM cifras ORDER BY data_insercao DESC")
                return cur.fetchall()
    except Exception as e:
        print("❌ Erro ao listar cifras:", e)
        return []

def buscar_cifra_por_id(cifra_id):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, titulo, autor, cifra FROM cifras WHERE id = %s", (cifra_id,))
                return cur.fetchone()
    except Exception as e:
        print("❌ Erro ao buscar cifra:", e)
        return None

