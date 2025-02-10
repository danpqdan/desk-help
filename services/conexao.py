import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from services.base import Base 

load_dotenv()

# Criando a classe Database
class Database:
    def __init__(self):
        self.database_url = f"mysql+pymysql://{os.getenv('USUARIO_DB')}:{os.getenv('SENHA_DB')}@localhost/{os.getenv('NOME_BANCO')}"
        self.engine = create_engine(self.database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def criar_tabelas(self):
        """Cria todas as tabelas no banco de dados se não existirem"""
        from model.Cliente import Cliente
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            Base.metadata.create_all(bind=self.engine)
            print("Tabelas criadas com sucesso!")
        else:
            print("As tabelas já existem no banco de dados.")

    def get_conexao(self):
        """Gera uma sessão de banco de dados"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()