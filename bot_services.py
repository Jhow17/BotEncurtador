import bot_repository

async def encurtar_url (url):
    
    resultado = await bot_repository.cadastra_url(url)
    if resultado is not None:
        hash_code = cria_hash(resultado[0])
        
        fk_url_original = resultado[0]
        
        url_encurtada = await bot_repository.cadastra_url_encurtada(f"https://encurtador.com/{hash_code}", hash_code, fk_url_original)
        
        if url_encurtada is not None:
            return url_encurtada[0]
    
    else:
        
        return None
    
def cria_hash(id):
    caracteres_base = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789+/'
    num = id
    base64_hash = ''
    while num > 0:
        resto  = num % 64 
        base64_hash += caracteres_base[resto]
        num = num // 64
    
    return base64_hash[::-1]
    
        
         
