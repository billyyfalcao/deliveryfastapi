from warnings import deprecated
import bcrypt
from fastapi import FastAPI
from passlib.context import CryptContext 
from dotenv import load_dotenv
import os

load_dotenv ()

SECRET_KEY = os.getenv ("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCES_TOKEN_EXPIRE_MINUTES = int (os.getenv ("ACCES_TOKEN_EXPIRE_MINUTES"))

app = FastAPI ()

bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

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