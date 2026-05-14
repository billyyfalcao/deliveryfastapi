from calendar import c

from sqlalchemy import column, create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base 

#para criar conexão com o banco
db = create_engine ("sqlite:///banco.db")

#cria a base do banco de dados 
Base = declarative_base()

#criar as classes 

class Usuario(Base):
    __tablename__ = "usuarios"

    id =  Column ("id", Integer, primary_key=True, autoincrement=True)
    nome = Column("nome", String)
    email = Column("email", String)
    senha = Column("senha",String)
    telefone = Column("telefone", Integer)
    ativo = Column("status",Boolean)
    admin = Column ("admin", Boolean, default=False)

    def __init__ (self, nome, email,senha,telefone,ativo,admin=False):
        
        self.nome = nome
        self.email = email
        self.senha = senha
        self.telefone = telefone
        self.ativo = ativo
        self.admin = admin

class Pedido(Base):
    __tablename__ = "pedidos"
        
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #PENDENTE, FINALIZADO, CANCELADO 
    usuario = Column("usuario", ForeignKey("usuario.id"))
    preco = Column("preco", Float)

    

#executar a criação dos metadados do seu banco (cria efetivamente o banco de dados)