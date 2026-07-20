
from http import HTTPStatus

from pydantic import _deprecated_dynamic_imports
from models import Usuario
from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from dependencies import pegar_sessao, verificar_token
from main import SECRET_KEY, bcrypt_context, ACCES_TOKEN_EXPIRE_MINUTES, ALGORITHM
from schemas import LoginSchema, UsuarioSchema
from sqlalchemy.orm import Session
from jose import jwt, JWTError
from datetime import datetime, timedelta, timezone


auth_router = APIRouter (prefix= "/auth", tags= ["auth"])

def criar_token (id_usuario, duracao_token = timedelta(minutes=ACCES_TOKEN_EXPIRE_MINUTES)):
    data_expiracao = datetime.now(timezone.utc) + duracao_token
    dic_info = {"sub": str(id_usuario), "exp": data_expiracao}
    jwt_encode = jwt.encode(dic_info, SECRET_KEY, ALGORITHM)
    return jwt_encode



def autenticar_usuario (email, senha, session):
    usuario = session.query(Usuario).filter(Usuario.email==email).first()
    if not usuario:
        return False
    elif not bcrypt_context.verify(senha, usuario.senha): 
        return False
    return usuario 


@auth_router.get("/")

async def autenticar():
    """
    Essa é a rota padrão de autenticação do nosso sistema. 
    """
    return {"Mensagem": "Você acessou a rota padrão de auenticação", "autenticado": False} 

@auth_router.post ("/criar_conta")
async def criar_conta(usuario_schema:UsuarioSchema, session: Session = Depends(pegar_sessao)):

    
    usuario = session.query(Usuario).filter(Usuario.email==usuario_schema.email).first()
    if usuario:
        # caso ja exista um usuario com esse email
        raise HTTPException(status_code=HTTPStatus.BAD_REQUEST, detail="já existe um usuario cadastrado com esse email!") 
    else:
        senha_criptografada = bcrypt_context.hash(usuario_schema.senha)
        novo_usuario = Usuario(usuario_schema.nome, usuario_schema.email, senha_criptografada, usuario_schema.telefone, usuario_schema.ativo, usuario_schema.admin)
        session.add(novo_usuario)
        session.commit()
        return {"mensagem": "usuário cadastrado com sucesso"}


@auth_router.post ("/login")
async def login (login_schema: LoginSchema, session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(login_schema.email, login_schema.senha, session)
    if not usuario:
        raise HTTPException (status_code=400, detail="Usuario não encontrado, verifique se as credenciais estão corretas")
    else:
        access_token = criar_token(usuario.id)
        refresh_token = criar_token(usuario.id, duracao_token=timedelta(days=7))
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "Bearer"
        }



@auth_router.post ("/login-form")
async def login_form (dados_formulario: OAuth2PasswordRequestForm = Depends(), session: Session = Depends(pegar_sessao)):
    usuario = autenticar_usuario(dados_formulario.username, dados_formulario.password, session)
    if not usuario:
        raise HTTPException (status_code=400, detail="Usuario não encontrado, verifique se as credenciais estão corretas")
    else:
        access_token = criar_token(usuario.id)
        return {
            "access_token": access_token,
            "token_type": "Bearer"
        }



@auth_router.get ("/refresh")
async def use_refresh_token (usuario: Usuario = Depends(verificar_token)):
    access_token = criar_token(usuario.id)

    return{
        "access_token": access_token,
        "token_type": "bearer"
    }