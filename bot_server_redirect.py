from fastapi import FastAPI, HTTPException
from fastapi.responses import RedirectResponse
import bot_services

app = FastAPI()

@app.get("/{hash_code}")
async def redirecionar(hash_code: str):
    
    url = await bot_services.acha_url(hash_code)
    print(f"URL encontrada: {url}")
    
    
    if url is None:
        raise HTTPException(status_code=404, detail="Ops! Esse link curto não existe ou foi apagado.")
    
   
    return RedirectResponse(url)