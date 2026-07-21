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


class ItemPedidoSchema(BaseModel):
    quantidade: int 
    sabor: str 
    tamanho: str 
    preco_unit: float

    class config: 
        from_attributes = True 