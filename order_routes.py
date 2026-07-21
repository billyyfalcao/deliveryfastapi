from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from dependencies import pegar_sessao, verificar_token
from schemas import PedidoSchema, ItemPedidoSchema
from models import Pedido, Usuario, ItemPedido

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


@order_router.post ("/pedido/cancelar/{id_pedido}")
async def cancelar_pedido (id_pedido: int, session: Session = Depends(pegar_sessao), usuario:Usuario = Depends (verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id == id_pedido).first()
    if not pedido:
        raise HTTPException(status_code=400, DETAIL = "Pedido não encontrado")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não tem autorização para cancelar este pedido")
    pedido.status = "CANCELADO" 
    session.commit()
    return {
        "mensagem": f"pedido numero {pedido.id} cancelado com sucesso>" ,
        "pedido": pedido  

    }


@order_router.get ("/listar")
async def listar_pedidos (session: Session = Depends(pegar_sessao), usuario: Usuario = Depends (verificar_token)):
    if not usuario.admin:
        raise HTTPException(status_code=401, detail= "Você não tem autorização para visualizar os pedidos")
    else: 
        pedidos = session.query (Pedido).all()
        return {
            "pedidos": pedidos
        }


@order_router.post("/pedido/adicionar/{id_pedido}")
async def adicionar_item_pedido(id_pedido:int, item_pedido_schema: ItemPedidoSchema, session: Session = Depends(pegar_sessao), usuario: Usuario =Depends(verificar_token)):
    pedido = session.query(Pedido).filter(Pedido.id==id_pedido).first()
    if not pedido: 
        raise HTTPException(status_code=400, detail="Pedido não existente")
    if not usuario.admin and usuario.id != pedido.usuario:
        raise HTTPException(status_code=401, detail="Você não possui autorização para adicionar itens a este pedido!")
    item_pedido = ItemPedido(item_pedido_schema.quantidade, item_pedido_schema.sabor,item_pedido_schema.tamanho,item_pedido_schema.preco_unit, id_pedido)

    
    session.add(item_pedido)
    pedido.calcular_preco()
    session.commit()
    return{
        "messagem": "Item criado com sucesso",
        "item_id": item_pedido.id,
        "preco_pedido": pedido.preco
    }
    
@order_router.delete("/pedido/remover/{id_item_pedido}")
async def remover_item_pedido(id_item_pedido:int, session: Session = Depends(pegar_sessao), usuario: Usuario =Depends(verificar_token)):
    item_pedido = session.query(ItemPedido).filter(ItemPedido.id==id_item_pedido).first()
    if not item_pedido: 
        raise HTTPException(status_code=404, detail="Item do pedido não existente")
    if not usuario.admin and usuario.id != item_pedido.pedido.usuario:
        raise HTTPException(status_code=403, detail="Você não possui autorização para remover itens a este pedido!")


    session.delete(item_pedido)
    session.commit()
    return{
        "mensagem": "Item removido com sucesso",
        "item_id": id_item_pedido,
        "preco_pedido": item_pedido.preco_unit
    }
    
    
