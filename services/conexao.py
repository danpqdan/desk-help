from contextlib import contextmanager
import os
import sys
from dotenv import load_dotenv
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
import urllib
from services.base import Base
from model.Cliente import Cliente
from model.ProdutoServico import ProdutoServico
from model.Vendedor import Vendedor
from services.router_path import help_desk_modelo_os


class Database:
    def __init__(self):
        self.carregar_env()
        senha_codificada = urllib.parse.quote_plus(str(self.senha_db))
        self.database_url = f"mysql+pymysql://{self.usuario_db}:{senha_codificada}@localhost/{self.nome_banco}"
        self.engine = create_engine(self.database_url, echo=True, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

    def carregar_env(self):
        """Carrega o arquivo .env correto dependendo do contexto do script"""
        if getattr(sys, 'frozen', False):
            base_dir = os.path.dirname(sys.executable)
        else:
            base_dir = os.path.dirname(os.path.abspath(__file__))

        dotenv_path = os.path.join(base_dir, '.env')
        
        if not os.path.exists(dotenv_path):
            raise FileNotFoundError(f"Arquivo .env não encontrado no diretório: {dotenv_path}")

        load_dotenv(dotenv_path=dotenv_path)

        self.usuario_db = os.getenv("USUARIO_DB")
        self.senha_db = os.getenv("SENHA_DB")
        self.nome_banco = os.getenv("NOME_BANCO")

        if not all([self.usuario_db, self.senha_db, self.nome_banco]):
            raise ValueError("As variáveis de ambiente do banco de dados não foram carregadas corretamente.")
        
    def criar_tabelas(self):
        """Cria todas as tabelas no banco de dados se não existirem"""
        from services.base import Base
        Base.metadata.create_all(bind=self.engine)
        print("Tabelas criadas com sucesso!")
        self.conversao_de_planilha()

    @contextmanager
    def get_conexao(self):
        """Gera uma sessão de banco de dados e garante o fechamento correto."""
        session = self.SessionLocal()
        try:
            yield session
            session.commit()
        except Exception as e:
            session.rollback()
            print(f"Erro na sessão do banco: {e}")
            raise
        finally:
            session.close()

    def conversao_de_planilha(self):
        """Converte uma planilha para o banco de dados"""
        try:
            with self.get_conexao() as session:
                clientes = pd.read_excel(help_desk_modelo_os, sheet_name='Clientes', header=1)
                produtos = pd.read_excel(help_desk_modelo_os, sheet_name='Produtos e Serviços', header=1)

                # Evita inserir dados duplicados
                if session.query(Cliente).first() is None:
                    session.bulk_insert_mappings(Cliente, clientes.to_dict(orient="records"))

                if session.query(ProdutoServico).first() is None:
                    session.bulk_insert_mappings(ProdutoServico, produtos.to_dict(orient="records"))

                # Criar usuários padrão caso não existam
                if session.query(Vendedor).count() < 3:
                    session.bulk_insert_mappings(Vendedor, [
                        {"email": "teste@teste.com", "nome": "admin", "senha": "admin", "usuario": "admin", "role": "admin"},
                        {"email": "teste2@teste.com", "nome": "Daniel S", "senha": "gerente", "usuario": "gerente", "role": "gerente"},
                        {"email": "teste1@teste.com", "nome": "Daniel S", "senha": "vendedor", "usuario": "vendedor", "role": "vendedor"},
                    ])
                print("Migração realizada com sucesso!")

        except Exception as e:
            print(f"Erro na conversão de planilha: {e}")
