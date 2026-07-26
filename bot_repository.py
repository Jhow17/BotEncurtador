import os 
import psycopg
import logging
from dotenv import load_dotenv
import sys
import asyncio

if sys.platform == 'win32':
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

load_dotenv()


string_conexao = f"dbname={os.getenv('DB_NAME')} user={os.getenv('DB_USER')} password={os.getenv('DB_PASS')} host={os.getenv('DB_HOST')} port={os.getenv('DB_PORT')}"



async def buscar_dados(query, parametros=None, buscar_todos=False):
    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, parametros)
                
                if buscar_todos:
                    return await cursor.fetchall()
                
                resultado = await cursor.fetchone()
                return resultado[0] if resultado else None
                
    except psycopg.Error as e:
        logging.error(f"Erro no banco ao buscar dados: {e}")
        return [] if buscar_todos else None

async def executar_query(query, parametros=None, retornar_id=False):

    try:
        async with await psycopg.AsyncConnection.connect(string_conexao) as conn:
            async with conn.cursor() as cursor:
                await cursor.execute(query, parametros)
                
                resultado = await cursor.fetchone()
                if resultado:
                    print(f"O resultado e esse {resultado}")
                    retorno = resultado
                        
                await conn.commit()
                return retorno 
                
    except psycopg.Error as e:
        logging.error(f"Erro no banco ao executar modificação: {e}")
        return None if retornar_id else False




async def buscar_todas_urls():
    return await buscar_dados("SELECT * FROM url_original;", buscar_todos=True)
            
async def buscar_todas_urls_encurtadas():
    return await buscar_dados("SELECT * FROM url_encurtada;", buscar_todos=True)

async def apagar_url(id_url):
    return await executar_query("DELETE FROM url_original WHERE id = %s;", (id_url,))

async def cadastra_url(url):
    return await executar_query(
        "INSERT INTO url_original (url_grande) VALUES (%s) RETURNING id;", 
        (url,), 
        retornar_id=True
    )
        
async def cadastra_url_encurtada(url_curta, hash_code, id_url_original):
    return await executar_query(
        "INSERT INTO url_encurtada (url_curta, hash_code, id_url_original) VALUES (%s,%s,%s) RETURNING url_curta;",
        (url_curta, hash_code, id_url_original),
        retornar_id=True
    )

async def acha_encurtada(hash_code):
    return await buscar_dados(
        "SELECT id_url_original FROM url_encurtada WHERE hash_code = %s;", 
        (hash_code,)
    )
    
async def acha_url_original(id_url):
    return await buscar_dados(
        "SELECT url_grande FROM url_original WHERE id = %s;", 
        (id_url,)
    )