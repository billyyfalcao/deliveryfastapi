from http import HTTPStatus
import bcrypt
from models import Usuario
from fastapi import APIRouter, Depends, HTTPException
from dependencies import pegar_sessao
from sqlalchemy.orm import sessionmaker
from main import bcrypt_context

auth_router = APIRouter (prefix= "/auth", tags= ["auth"])

@auth_router.get("/")

async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema. 
    """
    return {"Mensagem": "Você acessou a rota padrão de auenticação", "autenticado": False} 

@auth_router.post ("/criar_conta")
async def criar_conta(email:str, senha:str, nome: str, telefone: int, ativo: bool, admin:bool, session = Depends(pegar_sessao)):

    
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        # caso ja exista um usuario com esse email
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="já existe um usuario cadastrado com esse email!") 
    else:
        senha_criptografada = bcrypt_context.hash(senha)
        novo_usuario = Usuario(nome, email,senha_criptografada, telefone, ativo, admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}