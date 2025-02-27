import re
from sqlalchemy import Column, String
from services.base import Base

class Cliente(Base):
    __tablename__ = 'clientes'

    # Definindo os campos da tabela
    cpf = Column(String(11), primary_key=True)
    nome = Column(String(100), nullable=False)
    telefone = Column(String(15), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    def __repr__(self):
        return f"Cliente(cpf={self.cpf}, nome={self.nome}, telefone={self.telefone}, email={self.email})"
    
    def __init__(self, cpf:String, nome:String, telefone:String, email:String):
        self.cpf = self.limpar_cpf(cpf)
        self.nome = nome
        self.telefone = self.formatar_telefone(telefone)
        self.email = self.validar_email(email)
        
    def get_values(self):
        return (self.cpf, self.nome, self.telefone, self.email)
    
    @staticmethod
    def limpar_cpf(cpf: str) -> str:
        """Remove pontos e traços do CPF, mantendo apenas os números."""
        return re.sub(r'\D', '', cpf) 
    
    @staticmethod
    def validar_email(email: str) -> str:
        """Verifica se o e-mail tem um formato válido e retorna o e-mail se for válido."""
        padrao_email = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(padrao_email, email):
            raise ValueError("E-mail inválido!")
        return email

    @staticmethod
    def formatar_telefone(telefone: str) -> str:
        """Remove pontuações e formata o número no padrão DDD + número."""
        telefone_limpo = re.sub(r'\D', '', telefone)  # Remove tudo que não for número
        if len(telefone_limpo) == 11:  # Confere se tem o tamanho correto
            return telefone_limpo
        raise ValueError("Número de telefone inválido! Deve conter 11 dígitos.")


