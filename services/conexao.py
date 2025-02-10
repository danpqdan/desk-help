import os
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
import urllib
from services.base import Base
from model.Cliente import Cliente


load_dotenv()
senha_codificada = urllib.parse.quote_plus(os.getenv("SENHA_DB"))

# Criando a classe Database
class Database:
    def __init__(self):
        self.database_url = f"mysql+pymysql://{os.getenv('USUARIO_DB')}:{senha_codificada}@localhost/{os.getenv('NOME_BANCO')}"
        self.engine = create_engine(self.database_url, echo=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)
        

    def criar_tabelas(self):
        """Cria todas as tabelas no banco de dados se não existirem"""
        inspector = inspect(self.engine)
        existing_tables = inspector.get_table_names()

        if not existing_tables:
            Base.metadata.create_all(bind=self.engine)
            print("Tabelas criadas com sucesso!")
        else:
            print("As tabelas já existem no banco de dados.")
            
        self.adicionar_usuario_teste()

    def get_conexao(self):
        """Gera uma sessão de banco de dados"""
        db = self.SessionLocal()
        try:
            yield db
        finally:
            db.close()
            
    def adicionar_usuario_teste(self):
        """Adiciona um usuário de teste se não houver nenhum cadastrado"""
        session = self.SessionLocal()
        try:
            # Verifica se já existe um usuário no banco
            usuario_existente = session.query(Cliente).first()
            
            if not usuario_existente:
                novo_cliente = Cliente(
                    cpf="12345678901",
                    nome="admin",
                    telefone="(11) 99999-9999",
                    email="teste@email.com",
                    senha="admin"
                )
                session.add(novo_cliente)
                session.commit()
                print("Usuário de teste criado com sucesso!")
            else:
                print("Já existe um usuário no banco, nenhum novo foi adicionado.")
        
        except Exception as e:
            session.rollback()
            print(f"Erro ao criar usuário de teste: {e}")
        
        finally:
            session.close()
