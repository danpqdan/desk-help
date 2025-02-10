from sqlalchemy import Column, String
from services.base import Base


class Cliente(Base):
    __tablename__ = 'clientes'

    # Definindo os campos da tabela
    cpf = Column(String(11), primary_key=True)  # CPF como chave primária
    nome = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Cliente(cpf={self.cpf}, nome={self.nome}, telefone={self.telefone}, email={self.email})"
