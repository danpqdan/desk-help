from contextlib import contextmanager
import os
import pandas as pd
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError

from model.Cliente import Cliente
from model.ProdutoServico import ProdutoServico
from model.Vendedor import Vendedor

class Database:
    def __init__(self):
        self.database_url = f"mysql+pymysql://{os.getenv('USUARIO_DB')}:{os.getenv('SENHA_DB')}@localhost/{os.getenv('NOME_BANCO')}"
        self.engine = create_engine(self.database_url, echo=True, pool_pre_ping=True)
        self.SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=self.engine)

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
                clientes = pd.read_excel('assets/Planilha Modelo de Ordem de Serviço.xlsx', sheet_name='Clientes', header=1)
                produtos = pd.read_excel('assets/Planilha Modelo de Ordem de Serviço.xlsx', sheet_name='Produtos e Serviços', header=1)

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

    def encontrar_um(self, sql_query: str, params: dict = None):
        """Executa uma consulta SQL e retorna um resultado"""
        try:
            with self.get_conexao() as session:
                return session.execute(text(sql_query), params).fetchone()
        except SQLAlchemyError as e:
            print(f"Erro ao executar consulta: {e}")
            return None

    def encontrar_varios(self, sql_query: str, params: dict = None):
        """Executa uma consulta SQL e retorna múltiplos resultados"""
        try:
            with self.get_conexao() as session:
                resultado = session.execute(text(sql_query), params).fetchall()
                return resultado
        except SQLAlchemyError as e:
            print(f"Erro ao executar consulta: {e}")
            return []

    def executar(self, sql_text: str, params: dict = None):
        """Executa um comando SQL (INSERT, UPDATE, DELETE)"""
        try:
            with self.get_conexao() as session:
                session.execute(text(sql_text), params)
                return True
        except SQLAlchemyError as e:
            print(f"Erro ao executar a Query: {e}")
            return False
