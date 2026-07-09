from sqlalchemy import create_engine, Column, String, Integer, Boolean, Float, ForeignKey
from sqlalchemy.orm import declarative_base 
from sqlalchemy_utils.types import ChoiceType

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

  #  STATUS_PEDIDOS = (
  #     ("PENDENTE", "PENDENTE"),
  #     ("FINALIZADO", "FINALIZADO")
  #  )
        
    id = Column("id", Integer, primary_key=True, autoincrement=True)
    status = Column("status", String) #PENDENTE, FINALIZADO, CANCELADO 
    usuario = Column("usuario", ForeignKey("usuarios.id"))
    preco = Column("preco", Float)

    def __init__(self, usuario, status="PENDENTE", preco=0):
        self.usuario = usuario 
        self.preco = preco
        self.status = status


class ItemPedido (Base):
    __tablename__ = "itens_pedido"

    id = Column ( "id", Integer, primary_key=True, autoincrement=True)
    quantidade = Column ("quantidade", Integer)
    sabor = Column ("sabor", String)
    tamanho = Column ("tamanho", String)
    preco_unit = Column ("preco_unit", Float)
    pedido = Column ("pedido", ForeignKey ("pedidos.id"))

    def __init__ (self, quantidade, sabor, tamanho, preco_unit, pedido):
       self.quantidade = quantidade
       self.sabor = sabor 
       self.tamanho = tamanho 
       self.preco_unit = preco_unit
       self.pedido = pedido
       
#executar a criação dos metadados do seu banco (cria efetivamente o banco de dados)