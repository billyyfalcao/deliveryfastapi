from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao
from schemas import PedidoSchema
from models import Pedido

order_router = APIRouter (prefix= "/pedidos", tags = ["pedidos"])

@order_router.get("/")
async def pedidos():

    """
    Essa é a rota padrão de pedidos do nosso sistema. Todas as rotas dos pedidos precisam de autenticação
    """
    return {"Mensagem": "Você acessou a rota de pedidos!"}


@order_router.post("/pedido")
async def criar_pedido(pedido_schema: PedidoSchema, session: Session = Depends (pegar_sessao)):
    novo_pedido = Pedido (pedido_schema.usuario)
    session.add (novo_pedido)
    session.commit()
    return {"mensagem:": f"Pedido registrado com sucesso! Id do pedido: {novo_pedido.id}"}


@order_router.post ("/pedido/cancelar/ {novo_id.id}")
async def cancelar_pedido (id_pedido: int, session: Session = Depends(pegar_sessao)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, DETAIL = "Pedido não encontrado")
    pedido.status = "CANCELADO" 
    session.commit()
    return {
        "mensagem": f"pedido numerp {id_pedido} cancelado com sucesso>" ,
        "pedido": pedido 

    }
                    