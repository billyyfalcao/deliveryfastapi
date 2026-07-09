from http import HTTPStatus

from fastapi import APIRouter, HTTPException
from models import Usuario, db
from sqlalchemy.orm import sessionmaker

auth_router = APIRouter (prefix= "/auth", tags= ["auth"])

@auth_router.get("/")

async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema. 
    """
    return {"Mensagem": "Você acessou a rota padrão de auenticação", "autenticado": False} 

@auth_router.post ("/criar_conta")
async def criar_conta(email:str, senha:str, nome: str, telefone: int, ativo: bool, admin:bool):
    Session = sessionmaker(bind=db)
    session = Session ()
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if usuario:
        # caso ja exista um usuario com esse email
        raise HTTPException(status_code=HTTPStatus.CONFLICT, detail="já existe um usuario cadastrado com esse email!") 
    else:
        novo_usuario = Usuario(nome, email, senha, telefone, ativo, admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}