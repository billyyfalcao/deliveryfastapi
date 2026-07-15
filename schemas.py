from fastapi.security import OAuth2PasswordBearer
from pydantic import BaseModel 
from typing import Optional

class UsuarioSchema (BaseModel):
    nome: str 
    email: str
    senha: str
    telefone: int
    ativo: Optional [bool]
    admin: Optional [bool]

    class config:
        from_attributes = True 



class PedidoSchema (BaseModel):
    usuario: int
    
    class config: 
        from_attributes = True 


class LoginSchema (BaseModel):
    email: str 
    senha: str 

    class config: 
        from_attributes = True 


ouath2_scheme = OAuth2PasswordBearer(tokenUrl="/login")