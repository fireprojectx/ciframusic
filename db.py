import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def get_connection():
    return psycopg2.connect(os.getenv("DATABASE_URL"))

def criar_tabela_se_nao_existir():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("""
                    CREATE TABLE IF NOT EXISTS cifras (
                        id SERIAL PRIMARY KEY,
                        titulo TEXT,
                        autor TEXT,
                        cifra TEXT,
                        data_insercao TIMESTAMP DEFAULT NOW()
                    )
                """)
                conn.commit()
        print("✅ Tabela 'cifras' verificada/criada com sucesso.")
    except Exception as e:
        print("❌ Erro ao criar/verificar tabela:", e)

def salvar_cifra(titulo, autor, cifra):
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute(
                    "INSERT INTO cifras (titulo, autor, cifra) VALUES (%s, %s, %s)",
                    (titulo, autor, cifra)
                )
                conn.commit()
    except Exception as e:
        print("❌ Erro ao salvar cifra no banco:", e)

def listar_cifras():
    try:
        with get_connection() as conn:
            with conn.cursor() as cur:
                cur.execute("SELECT id, titulo, autor FROM cifras ORDER BY id DESC")
                return cur.fetchall()
    except Exception as e:
        print("❌ Erro ao listar cifras:", e)
        return []
    
def buscar_cifra_por_titulo(titulo):
    try:
        conn = get_connection()
        cur = conn.cursor()
        cur.execute("SELECT titulo, autor, cifra FROM cifras WHERE titulo = %s", (titulo,))
        resultado = cur.fetchone()
        cur.close()
        conn.close()

        if resultado:
            return {
                "titulo": resultado[0],
                "autor": resultado[1],
                "cifra": resultado[2]
            }
        return None
    except Exception as e:
        print("❌ Erro ao buscar cifra por título:", e)
        return None

