from fastapi import FastAPI

app = FastAPI ()

from auth_routes import auth_router 
from order_routes import order_router 

app.include_router(auth_router)
app.include_router (order_router)




# comando para rodar o codigo: uvicorn main:app --reload

#endpoint: 
# /ordens 
# /auth
# /login 

#Requisição - Rest APIs

#Get -> Leitura/ pegar 
#Post -> enviar/ criar 
#Put/Patch -> edição 
#Delete -> deletar 