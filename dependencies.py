from models import db
from sqlalchemy.orm import sessionmaker

def pegar_sessao():
    try: 
         Session = sessionmaker  (bind = db) 
         session = Session()
         return session 
    finally:
         session.close()
    