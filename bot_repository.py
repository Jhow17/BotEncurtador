import os 
import psycopg
import logging
from dotenv import load_dotenv
import sys
import asyncio

# Força o Windows a usar o motor assíncrono compatível com o Psycopg
if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()

NAME = os.getenv('DB_NAME')
USER = os.getenv('DB_USER')
PASS = os.getenv('DB_PASS')
HOST = os.getenv('DB_HOST')
PORT = os.getenv('DB_PORT')

string_conexao = f"dbname={NAME} user={USER} password={PASS} host={HOST} port={PORT}"
print(string_conexao)

async def buscar_todas_urls():
    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM url_original;")
                return await cursor.fetchall()
    except psycopg.Error as e:
        logging.error(f"Falha na conexão ou consulta ao banco de dados: {e}")
        return []
            
async def buscar_todas_urls_encurtadas():
    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("SELECT * FROM url_encurtada;")
                return await cursor.fetchall()
    except psycopg.Error as e:
        logging.error(f"Falha ao buscar URLs encurtadas: {e}")
        return []

async def apagar_url(id_url):
    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute("DELETE FROM url_original WHERE id = %s;", (id_url,))
                await conn.commit()
                return True 
    except psycopg.Error as e:
        logging.error(f"Falha ao apagar URL (ID {id_url}): {e}")
        return False

async def adicionar_url(url):
    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(
                    "INSERT INTO url_original (url_grande) VALUES (%s) RETURNING id;", 
                    (url,)
                )
                
                resultado = await cursor.fetchone()
                 
                await conn.commit()
                
                return resultado[0]
                
    except psycopg.Error as e:
        print(e)
        logging.error(f"Falha ao adicionar URL {url}")
        return None
        


