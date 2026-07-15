from models import db
from sqlalchemy.orm import sessionmaker, Session
from models import Usuario
from fastapi import Depends, HTTPException, security
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from main import SECRET_KEY, ALGORITHM




def pegar_sessao():
    try: 
         Session = sessionmaker  (bind = db) 
         session = Session()
         yield session 
    finally:
         session.close()


ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def verificar_token (token: str = Depends(ouath2_scheme), session:Session= Depends(pegar_sessao)):

    usuario_id = session.query(Usuario).filter(Usuario.id).first()

    try:
        payload = jwt.decode(
            token, 
            SECRET_KEY,
            algorithms=[ALGORITHM]
        )

        usuario_id = payload.get("sub")

        if usuario_id is None:
            raise HTTPException(
                status_code=401, detail="Token invalido"
            )

                                    
        return usuario_id

    except JWTError: 
        raise HTTPException(
            status_code=401, detail="token inválido"
        ) 