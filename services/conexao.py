import os
import urllib
import pandas as pd
from sqlalchemy import create_engine, inspect
from sqlalchemy.sql import text
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv
from services.base import Base
from model.Sacola import Sacola, SacolaProduto
from model.ProdutoServico import ProdutoServico, TipoProdutoServico
from model.Cliente import Cliente
from model.Vendedor import Vendedor


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
        Base.metadata.create_all(bind=self.engine)
        print("Tabelas criadas com sucesso!")
        self.conversao_de_planilha()


    def get_conexao(self):
        """Gera uma sessão de banco de dados e retorna a instância"""
        db = self.SessionLocal()
        return db
            
    def conversao_de_planilha(self):
        """Adiciona um usuário de teste se não houver nenhum cadastrado"""
        session = self.SessionLocal()
        try:
            clientes = pd.read_excel('assets/Planilha Modelo de Ordem de Serviço.xlsx', sheet_name='Clientes', header=1)
            produtos = pd.read_excel('assets/Planilha Modelo de Ordem de Serviço.xlsx', sheet_name='Produtos e Serviços', header=1)
            
            vendedor_existente = session.query(Vendedor).first()
            cliente_existente = session.query(Cliente).first()
            produto_existente = session.query(ProdutoServico).first()
            
            if not produto_existente:
                for _, linha in produtos.iterrows():
                    tipo_normalizado = str(linha['Tipo']).strip().upper()
                    if tipo_normalizado == 'SERVICO':
                        tipo_normalizado = 'SERVIÇO'
                    novo_produto = ProdutoServico(
                        codigo=linha['Código'],
                        descricao=linha['Descrição'],
                        tipo=tipo_normalizado,
                        valor=linha['Valor']
                    )
                    novo_produto.__repr__()
                    session.add(novo_produto)

                session.commit()

            elif not cliente_existente:
                for _, linha in clientes.iterrows():
                    novo_cliente = Cliente(
                        cpf=linha['CPF'],
                        nome=linha['NOME'],
                        telefone=linha['TELEFONE'],
                        email=linha['E-MAIL']
                    )
                    novo_cliente.__repr__()
                    session.add(novo_cliente)

                session.commit()

            elif not vendedor_existente:
                novo_vendedor = Vendedor(
                    email="teste@teste.com",
                    nome="admin",
                    senha="admin",
                    usuario="admin"
                )
                novo_vendedor.__repr__()
                session.add(novo_vendedor)
                session.commit()

            print("Migração realizada com sucesso!")

        except Exception as e:
            session.rollback()
            print(f"Erro na conversão de planilha: {e}")

        finally:
            session.close()



    def encontrar_um(self, sql_query: str, params: dict = None):
        """Executa uma consulta SQL e retorna apenas um resultado."""
        try:
            with self.get_conexao() as session:
                resultado = session.execute(text(sql_query), params).fetchone()
                return resultado
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return None
        finally:
            session.close()

    def encontrar_varios(self, sql_query: str, params: dict = None):
        """Executa uma consulta SQL e retorna uma lista de resultados."""
        try:
            with self.get_conexao() as session:
                resultado = session.execute(text(sql_query), params).fetchall()
                return resultado
        except Exception as e:
            print(f"Erro ao executar consulta: {e}")
            return []
        finally:
            session.close()